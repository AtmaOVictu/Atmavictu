use std::fs;
use uuid::Uuid;

#[test]
fn bundle_preview_rejects_file_tampering_and_traversal() {
    let root = std::env::temp_dir().join(format!("bundle-validate-{}", Uuid::new_v4()));
    fs::create_dir_all(&root).unwrap();
    let result = (|| -> Result<(), String> {
        fs::write(root.join("book.workbench.json"), "{}\n").map_err(|e| e.to_string())?;
        let bundle = export_project(&root)?;
        let parsed: ProjectBundle = super::parse(&bundle)?;
        let mut tampered = parsed.clone();
        if let Some(file) = tampered.files.first_mut() { file.content.push_str("tamper"); }
        let text = serde_json::to_string(&tampered).map_err(|e| e.to_string())?;
        assert!(!validate(&parse(&text)?)?.valid);
        let mut escaped = parsed;
        if let Some(file) = escaped.files.first_mut() { file.path = "../escape".into(); file.sha256 = sha(file.content.as_bytes()); }
        escaped.sha256 = serde_json::from_str::<ProjectBundle>(&super::seal_bundle(escaped.clone())?).map_err(|e| e.to_string())?.sha256;
        assert!(!validate(&escaped)?.valid);
        Ok(())
    })();
    let _ = fs::remove_dir_all(root);
    result.unwrap();
}

#[test]
fn restore_refuses_collisions_unless_explicitly_confirmed() {
    let root = std::env::temp_dir().join(format!("bundle-restore-{}", Uuid::new_v4()));
    fs::create_dir_all(&root).unwrap();
    let result = (|| -> Result<(), String> {
        let bundle = ProjectBundle { format: "atmavictu-project-bundle-v1".into(), created_at: "now".into(), files: vec![add_file("note.txt", "bundle".into())], sha256: String::new() };
        let text = seal_bundle(bundle)?;
        fs::write(root.join("note.txt"), "keep").map_err(|e| e.to_string())?;
        assert!(restore_project(&root, &text, false).is_err());
        assert_eq!(fs::read_to_string(root.join("note.txt")).map_err(|e| e.to_string())?, "keep");
        restore_project(&root, &text, true)?;
        assert_eq!(fs::read_to_string(root.join("note.txt")).map_err(|e| e.to_string())?, "bundle");
        Ok(())
    })();
    let _ = fs::remove_dir_all(root);
    result.unwrap();
}
