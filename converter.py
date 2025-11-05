import os
import re
from PIL import Image, ExifTags, UnidentifiedImageError
from pillow_heif import register_heif_opener
from datetime import datetime
import piexif
import fnmatch
from typing import List, Callable, Optional, Union, Tuple
import zipfile
import threading

register_heif_opener(allow_incorrect_headers=True)


def generate_unique_filename(target_file: str) -> str:
    """
    Generate a unique filename by adding (n) suffix if file exists

    :param target_file: The target file path
    :return: A unique file path that doesn't exist
    """
    if not os.path.exists(target_file):
        return target_file

    directory = os.path.dirname(target_file)
    filename, extension = os.path.splitext(os.path.basename(target_file))

    # Check if filename already has (n) pattern
    match = re.match(r"(.*)\((\d+)\)$", filename)
    if match:
        base_name = match.group(1).rstrip()
        counter = int(match.group(2))
    else:
        base_name = filename
        counter = 1

    # Find an available filename
    while True:
        new_filename = f"{base_name}({counter}){extension}"
        new_path = os.path.join(directory, new_filename)
        if not os.path.exists(new_path):
            return new_path
        counter += 1


def get_file_list(dir_of_interest: str, recursive: bool) -> List[List[str]]:
    """
    Get a list of all HEIC files in the directory of interest

    :param dir_of_interest: the directory to search
    :param recursive: search subdirectories
    :return: a list of files as [path, filename] pairs
    """
    file_list = []

    if os.path.isdir(dir_of_interest):
        for root, dirs, files in os.walk(dir_of_interest):
            if not recursive:
                dirs.clear()
            for file in files:
                if fnmatch.fnmatch(file.lower(), '*.heic'):
                    file_list.append([os.path.normpath(root), file])
        return file_list
    else:
        print("Path {} is not a valid directory.".format(dir_of_interest))
        return []


def convert_heic_file(
        source_file: str,
        target_file: str,
        overwrite: bool,
        remove: bool,
        quality: int,
        progress_callback: Optional[Callable[[str], None]] = None,
        verbose: bool = False
) -> bool:
    """
    Convert a single heic file to jpeg

    :param source_file: the source file
    :param target_file: the target file
    :param overwrite: overwrite existing jpeg files
    :param remove: remove converted heic files
    :param quality: quality of jpeg files (1-100)
    :param progress_callback: optional callback for progress updates
    :param verbose: enable more detailed output
    :return: True if successful, False otherwise
    """
    # Validate inputs
    if not os.path.isfile(source_file):
        if verbose:
            print(f"Source file {source_file} does not exist")
        return False

    if not source_file.lower().endswith('.heic'):
        if verbose:
            print(f"Source file {source_file} is not a HEIC file")
        return False

    # Normalize quality
    quality = max(1, min(100, quality))

    # Report progress if callback provided
    if progress_callback:
        progress_callback(f"Converting {os.path.basename(source_file)}")

    # Check if target folder exists
    target_folder = os.path.dirname(target_file)
    if not os.path.exists(target_folder):
        if verbose:
            print(f'Creating folder {target_folder}')
        os.makedirs(target_folder)

    if os.path.exists(target_file) and not overwrite:
        if verbose:
            print(f'File {target_file} already exists, skip')
        return False

    try:
        image = Image.open(source_file)
        image_exif = image.getexif()

        exif_dict = {"0th": {}, "Exif": {}, "GPS": {}, "1st": {}}

        if image_exif:
            # Make a map with tag names and grab the datetime
            exif = {ExifTags.TAGS[k]: v for k, v in image_exif.items() if k in ExifTags.TAGS and type(v) is not bytes}
            if 'DateTime' in exif:
                date = datetime.strptime(exif['DateTime'], '%Y:%m:%d %H:%M:%S')
            else:
                date = datetime.now()

            # Try to load existing exif data via piexif
            try:
                if "exif" in image.info:
                    exif_dict = piexif.load(image.info["exif"])
            except:
                # If loading fails, use our default structure
                pass
        else:
            # No EXIF data exists, use current datetime
            date = datetime.now()
            if verbose:
                print(f'No EXIF data found for {source_file}, creating dummy EXIF data')

        # Update exif data with orientation and datetime
        exif_dict["0th"][piexif.ImageIFD.DateTime] = date.strftime("%Y:%m:%d %H:%M:%S")
        exif_dict["0th"][piexif.ImageIFD.Orientation] = 1

        # Add dummy author data to ensure EXIF is not empty
        exif_dict["0th"][piexif.ImageIFD.Artist] = "unknown"

        # Ensure the Exif IFD exists and add a dummy entry if needed
        if not exif_dict.get("Exif"):
            exif_dict["Exif"] = {}

        exif_bytes = piexif.dump(exif_dict)

        # Save image as jpeg
        image.save(target_file, "jpeg", exif=exif_bytes, quality=quality)
        if verbose:
            print(f'Converted image: {source_file} -> {target_file}')
        if remove:
            os.remove(source_file)
            if verbose:
                print(f'Removed original: {source_file}')

        # Report success if callback provided
        if progress_callback:
            progress_callback(f"Successfully converted {os.path.basename(source_file)}")

        return True

    except UnidentifiedImageError as e:
        print(f"{source_file} is not a valid image: {e}")
    except Exception as e:
        print(f"Unable to convert {source_file}: {e}")

    # Report failure if callback provided
    if progress_callback:
        progress_callback(f"Failed to convert {os.path.basename(source_file)}")

    return False


def convert_multiple_heic_files(
        file_list: List[str],
        overwrite: bool,
        remove: bool,
        quality: int,
        target: str,
        progress_callback: Optional[Callable[[str], None]] = None,
        generate_unique: bool = False,
        verbose: bool = False
) -> List[str]:
    """
    Convert a list of HEIC files to JPEG

    :param file_list: List of HEIC file paths
    :param overwrite: Overwrite existing JPEG files
    :param remove: Remove converted HEIC files
    :param quality: Quality of JPEG files
    :param target: Target directory
    :param progress_callback: Optional callback for progress updates
    :param generate_unique: Generate unique filenames when target exists
    :param verbose: Enable more detailed output

    :return: List of successfully converted files
    """
    success_files = []

    if verbose:
        print(f'Processing {len(file_list)} files')

    for source_file in file_list:
        if not os.path.isfile(source_file) or not source_file.lower().endswith('.heic'):
            if verbose:
                print(f'Skipping invalid file: {source_file}')
            continue

        target_filename = os.path.basename(source_file).split('.')[0] + ".jpg"
        target_file = os.path.join(target, target_filename)

        # Generate unique filename if requested and not overwriting
        if generate_unique and not overwrite and os.path.exists(target_file):
            target_file = generate_unique_filename(target_file)
            if verbose:
                print(f'Generated unique name: {os.path.basename(target_file)}')

        if convert_heic_file(
                source_file,
                target_file,
                overwrite,
                remove,
                quality,
                progress_callback,
                verbose
        ):
            success_files.append(os.path.basename(target_file))

    return success_files


def convert_heic_to_jpeg(
        dir_of_interest: str,
        recursive: bool,
        overwrite: bool,
        remove: bool,
        quality: int,
        target: str,
        preserve_folder_structure: bool = True,
        progress_callback: Optional[Callable[[str], None]] = None,
        generate_unique: bool = False,
        verbose: bool = False,
) -> List[str]:
    """
    Convert all heic files in the directory of interest to jpeg

    :param dir_of_interest: The directory to search
    :param recursive: search subdirectories
    :param overwrite: overwrite existing jpeg files
    :param remove: remove converted heic files
    :param quality: quality of jpeg files
    :param target: the target directory
    :param preserve_folder_structure creates a folder structure
    :param progress_callback: Optional callback for progress updates
    :param generate_unique: Generate unique filenames when target exists
    :param verbose: Enable more detailed output

    :return: a list of successfully converted files
    """
    heic_files = get_file_list(dir_of_interest, recursive)

    # Extract files of interest
    success_files = []

    if verbose:
        print(f'Found {len(heic_files)} files to convert in folder {dir_of_interest}')

    # Convert files to jpg while keeping the timestamp
    for root, filename in heic_files:

        dir_prefix = ''
        if preserve_folder_structure:
            dir_prefix = os.path.relpath(root, dir_of_interest)
            if dir_prefix != '.':
                os.makedirs(os.path.join(target, dir_prefix), exist_ok=True)
            else:
                dir_prefix = ''

        target_filename = os.path.join(dir_prefix, os.path.splitext(filename)[0] + ".jpg")
        target_file = os.path.join(target, target_filename)
        source_file = os.path.join(root, filename)

        # Generate unique filename if requested and not overwriting
        if generate_unique and not overwrite and os.path.exists(target_file):
            target_file = generate_unique_filename(target_file)
            if verbose:
                print(f'Generated unique name: {os.path.basename(target_file)}')

        if convert_heic_file(source_file, target_file, overwrite, remove, quality, progress_callback, verbose):
            success_files.append(os.path.basename(target_file))

    return success_files

def delete_file(file_path):
    """
    Delete a file
    :param file_path:  full path of file to delete
    """
    if os.path.exists(file_path):
        try:
            os.remove(file_path)
            print(f"delete file OK: {file_path}")
        except Exception as e:
            print(f"delete file error: {e}")

def convert_livp_to_jpeg(
        livp_file: str,
        output_file: str,
        overwrite: bool,
        quality: int):
    """
    Convert a single livp file to jpeg
    :param livp_file:  full path of xxx.livp
    :param output_file: full path of output jpeg file
    :param overwrite: overwrite existing jpeg files
    :param quality: quality of jpeg file(1-100)
    """
    output_dir = os.path.dirname(output_file)
    # 提取HEIC文件
    with zipfile.ZipFile(livp_file, 'r') as zip_ref:
        heic_files = [name for name in zip_ref.namelist() if name.endswith('.heic')]
        if not heic_files:
            print("Can not find HEIC from Live Photo!!!")
            return False
        heic_file = heic_files[0]
        zip_ref.extract(heic_file, output_dir)
        heic_path = os.path.join(output_dir, heic_file)
        result = convert_heic_file(heic_path, output_file, overwrite, False, quality)
        # 延时1秒后，删除解压出来的heic文件
        timer = threading.Timer(1, delete_file, args=[heic_path])
        timer.start()

    return result


def scan_files(path, suffix=None):
    """
    递归获取文件夹所有文件,可过滤匹配指定后缀名suffix的文件.
    返回包含全路径的文件列表
    :param path: 要扫描的路径
    :param suffix:后缀名包含点,例如: .jpg
    """
    result = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if suffix is not None:
                if file.endswith(suffix):
                    result.append(os.path.join(root, file))
            else:
                result.append(os.path.join(root, file))
    return result
