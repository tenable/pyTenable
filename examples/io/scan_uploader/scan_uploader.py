#!/usr/bin/env python
from typing import Optional
from pathlib import Path
from tenable.io import TenableIO
from rich import print
import typer


app = typer.Typer()


@app.command()
def uploader(path: Path,
             access_key: Optional[str] = None,
             secret_key: Optional[str] = None,
             aggregate: bool = True,
             ):
    """
    Uploads all of the .nessus files in the specified folder into
    Tenable Vulnerability Management
    """
    tio = TenableIO(access_key=access_key, secret_key=secret_key)

    def upload_to_tvm(filename: Path):
        """Uploads the file to TVM"""
        if filename.suffix.lower() == '.nessus':
            with filename.open('rb') as scanobj:
                print(f'Uploading {filename} into TVM...')
                tio.scans.import_scan(scanobj)

    # If the path is a single file and has a .nessus suiffix, then we will
    # simply upload the file into TVM.
    if not path.is_dir() and path.suffix().lower() == '.nessus':
        upload_to_tvm(path)

    # If the path is a directory, then we will iterate over the files in the
    # directory (non-recursively) and every file with a .nessus suffix will
    # be uploaded into TVM.
    elif path.is_dir():
        for file_path in path.iterdir():
            upload_to_tvm(file_path)

    # The path isn't correct.  Inform the user and bail.
    else:
        print(f'Invalid path {path}')


if __name__ == '__main__':
    app()
