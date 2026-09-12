#!/usr/bin/env python3
import nibabel as nib
import os
from geometry_guard import require_same_grid

def copy_geometry(source_file, target_file, output_file):
    """Copy only an already matching grid; never repair geometry by header swapping."""
    if os.path.exists(output_file):
        raise FileExistsError('Refusing to overwrite an existing image')
    print(f"Processing: {os.path.basename(source_file)}")
    
    # 加载图像
    source_img = nib.load(source_file)
    target_img = nib.load(target_file)

    require_same_grid(source_img.shape, source_img.affine,
                      target_img.shape, target_img.affine)
    # Preserve source metadata and values; matching grids need no header replacement.
    nib.save(source_img, output_file)
    print(f"Saved to: {output_file}")

# 使用示例
if __name__ == "__main__":
    raise SystemExit('Automatic batch header replacement is disabled. Use an explicit validated registration workflow.')
