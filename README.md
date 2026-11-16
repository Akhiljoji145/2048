# 2048 Windows Desktop

A standalone 2048 desktop game for Windows.

## Controls
- Arrow keys: move tiles
- U: undo last move
- R: restart
- On-screen New Game and Undo buttons

Best score is saved locally in your Windows user folder.

## Build the EXE with GitHub Actions
1. Create a GitHub repository.
2. Upload everything in this folder to the repository root, including `.github`.
3. Open Actions and choose **Build 2048 Windows EXE**.
4. Click **Run workflow**.
5. When the workflow finishes, download the **2048-Windows-EXE** artifact.
6. Extract it and run `2048-Desktop.exe`.

The ZIP contains source code and a Windows build workflow; it is not itself a compiled EXE.
