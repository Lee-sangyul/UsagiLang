# Publish UsagiLang to GitHub

The ChatGPT GitHub connector currently supports writing **files to an existing repo**, but not creating a new repo. The repository must first exist.

1. Open https://github.com/new and sign in as `Lee-sangyul`.
2. Repository name: `UsagiLang`; visibility: **Public**.
3. **Do not** initialize README, .gitignore, or license: this project includes all three.
4. Create the repository.
5. In a terminal in this unzipped folder, run:

```bash
git init -b main
git add .
git commit -m "feat: release UsagiLang v0.1.0-alpha"
git remote add origin https://github.com/Lee-sangyul/UsagiLang.git
git push -u origin main
git tag v0.1.0-alpha
git push origin v0.1.0-alpha
```

6. On https://github.com/Lee-sangyul/UsagiLang/releases/new, select the tag `v0.1.0-alpha` and check **Set as a pre-release**. Add highlights from `CHANGELOG.md`.

Alternative: after step 4, ask ChatGPT to upload the project to the existing repository using the connected GitHub account. Do not do both methods or you may get duplicate/competing commits.

The repo is a **fan-made, unofficial experimental programming language** and must not be represented as associated with the original fictional franchise's rights holders.