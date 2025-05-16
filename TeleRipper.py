#!/usr/bin/env python3
import os
import sys
import argparse
import configparser
import getpass
from pathlib import Path
from telethon.sync import TelegramClient
from telethon.errors import RPCError
from telethon.tl.types import MessageMediaDocument, DocumentAttributeVideo

def create_config_if_not_exists():
    """Create config file if it doesn't exist and prompt for API credentials"""
    config_dir = Path.home() / '.teleripper'
    config_file = config_dir / 'config.ini'
    
    # Create directory if it doesn't exist
    if not config_dir.exists():
        config_dir.mkdir(parents=True)
    
    config = configparser.ConfigParser()
    
    # Check if config file exists
    if not config_file.exists():
        print("No configuration found. Let's set up your API credentials.")
        print("You can get these from https://my.telegram.org/apps")
        
        api_id = input("Enter your API ID: ")
        api_hash = getpass.getpass("Enter your API Hash: ")
        
        config['Telegram'] = {
            'api_id': api_id,
            'api_hash': api_hash,
            'session_name': 'TeleRipper'
        }
        
        with open(config_file, 'w') as f:
            config.write(f)
        
        print(f"Configuration saved to {config_file}")
        return api_id, api_hash, 'TeleRipper'
    
    # Read existing config
    config.read(config_file)
    if 'Telegram' in config:
        return (
            config['Telegram'].get('api_id'),
            config['Telegram'].get('api_hash'),
            config['Telegram'].get('session_name', 'TeleRipper')
        )
    else:
        print("Invalid config file. Please delete ~/.teleripper/config.ini and run again.")
        sys.exit(1)

def list_channels(client):
    """List all channels the user has joined"""
    print("Channels your account has joined:")
    print("-" * 50)
    print(f"{'Channel Name':<40} {'Channel ID':<15}")
    print("-" * 50)
    
    channels = []
    
    for dialog in client.iter_dialogs():
        if dialog.is_channel:
            channel = dialog.entity
            channel_id = channel.id
            if channel_id < 0:
                # Ensure proper formatting for public display
                formatted_id = f"-100{abs(channel_id)}" if not str(channel_id).startswith('-100') else str(channel_id)
            else:
                formatted_id = str(channel_id)
            print(f"{channel.title:<40} {formatted_id:<15}")
            channels.append((channel.title, formatted_id))
    
    return channels

def download_media(client, channel_id, download_dir=None, limit=None, media_types=None):
    """Download media files from specified channel including videos, photos, documents, etc."""
    # Default to all media types if none specified
    if media_types is None:
        media_types = ['all']  # 'all' means download everything
    
    if download_dir is None:
        download_dir = 'downloaded_media'
    
    os.makedirs(download_dir, exist_ok=True)
    
    # Define common file extensions for categorization
    extension_categories = {
        # Videos
        'mp4': 'videos', 'avi': 'videos', 'mkv': 'videos', 'mov': 'videos', 'wmv': 'videos',
        'flv': 'videos', 'webm': 'videos', '3gp': 'videos', 'm4v': 'videos',
        # Images
        'jpg': 'images', 'jpeg': 'images', 'png': 'images', 'gif': 'images', 
        'bmp': 'images', 'webp': 'images', 'svg': 'images', 'tiff': 'images',
        # Documents
        'pdf': 'documents', 'doc': 'documents', 'docx': 'documents', 
        'xls': 'documents', 'xlsx': 'documents', 'ppt': 'documents', 'pptx': 'documents',
        'txt': 'documents', 'rtf': 'documents', 'odt': 'documents',
        # Audio
        'mp3': 'audio', 'wav': 'audio', 'ogg': 'audio', 'flac': 'audio', 
        'm4a': 'audio', 'aac': 'audio', 'wma': 'audio',
        # Archives
        'zip': 'archives', 'rar': 'archives', '7z': 'archives', 'tar': 'archives', 
        'gz': 'archives', 'bz2': 'archives',
        # Other common file types
        'exe': 'programs', 'apk': 'programs', 'iso': 'programs',
        'json': 'data', 'xml': 'data', 'csv': 'data', 'sql': 'data',
        'html': 'web', 'css': 'web', 'js': 'web'
    }
    
    try:
        # Make sure channel_id is properly formatted
        try:
            # If it's already a correctly formatted ID, just use it
            entity = client.get_entity(channel_id)
        except ValueError:
            # Try to format it correctly if needed
            if isinstance(channel_id, str) and not channel_id.startswith('-100'):
                if channel_id.startswith('-'):
                    # It might be missing the '100' prefix
                    channel_id = f"-100{channel_id[1:]}"
                else:
                    # It might be a plain number
                    channel_id = f"-100{channel_id}"
                
            try:
                entity = client.get_entity(int(channel_id))
            except:
                print(f"Error: Could not find channel with ID {channel_id}.")
                print("Use --lc to list channels with their correct IDs.")
                return
        
        channel_name = entity.title
        print(f"Downloading media from channel: {channel_name} ({channel_id})")
        
        sanitized_name = ''.join(c if c.isalnum() or c in ' _-' else '_' for c in channel_name)
        
        # Create a subfolder with the channel name
        channel_dir = os.path.join(download_dir, sanitized_name)
        os.makedirs(channel_dir, exist_ok=True)
        
        # Create category directories
        category_dirs = {}
        for category in set(extension_categories.values()):
            category_dir = os.path.join(channel_dir, category)
            os.makedirs(category_dir, exist_ok=True)
            category_dirs[category] = category_dir
        
        # Also create a directory for uncategorized files
        uncategorized_dir = os.path.join(channel_dir, 'other')
        os.makedirs(uncategorized_dir, exist_ok=True)
        
        # Prepare iterator with optional limit
        if limit:
            messages = client.iter_messages(entity, limit=int(limit))
        else:
            messages = client.iter_messages(entity)
        
        # Initialize counters for each category
        counts = {category: 0 for category in set(extension_categories.values())}
        counts['other'] = 0
        total_count = 0
        
        for message in messages:
            # Skip messages without media
            if not message.media:
                continue
                
            # Handle photos (they have a special case in Telegram API)
            if hasattr(message.media, 'photo') and message.media.photo:
                if 'all' in media_types or 'images' in media_types:
                    counts['images'] += 1
                    date_str = message.date.strftime("%Y%m%d")
                    filename = f"photo_{date_str}_{message.id}.jpg"
                    file_path = os.path.join(category_dirs['images'], filename)
                    
                    # Check if file already exists
                    if os.path.exists(file_path):
                        print(f"File already exists, skipping: {filename}")
                        continue
                    
                    print(f"Downloading image #{counts['images']}: {filename}...")
                    try:
                        client.download_media(message, file=file_path)
                        print(f"Successfully downloaded: {filename}")
                        total_count += 1
                    except Exception as e:
                        print(f"Error downloading {filename}: {e}")
            
            # Handle documents (videos, files, etc.)
            elif isinstance(message.media, MessageMediaDocument):
                # Get the document's attributes
                attributes = message.media.document.attributes
                mime_type = getattr(message.media.document, 'mime_type', 'application/octet-stream')
                
                # Try to get the filename from attributes
                filename = None
                for attr in attributes:
                    if hasattr(attr, 'file_name') and attr.file_name:
                        filename = attr.file_name
                        break
                
                # If no filename, create one based on message data
                if not filename:
                    date_str = message.date.strftime("%Y%m%d")
                    # Try to determine extension from mime_type
                    extension = mime_type.split('/')[-1] if '/' in mime_type else 'bin'
                    if extension == 'jpeg':
                        extension = 'jpg'
                    elif extension == 'quicktime':
                        extension = 'mov'
                    filename = f"file_{date_str}_{message.id}.{extension}"
                
                # Determine the file category
                file_ext = filename.split('.')[-1].lower() if '.' in filename else ''
                category = extension_categories.get(file_ext, 'other')
                
                # Special case for videos (check attributes as well as extension)
                is_video = any(
                    isinstance(attr, DocumentAttributeVideo) and not attr.round_message
                    for attr in attributes
                )
                if is_video:
                    category = 'videos'
                
                # Check if we want to download this type of media
                if 'all' in media_types or category in media_types:
                    # Increment the counter for this category
                    counts[category] += 1
                    
                    # Determine the directory based on category
                    if category in category_dirs:
                        target_dir = category_dirs[category]
                    else:
                        target_dir = uncategorized_dir
                    
                    # Full path for the file
                    file_path = os.path.join(target_dir, filename)
                    
                    # Check if file already exists
                    if os.path.exists(file_path):
                        print(f"File already exists, skipping: {filename}")
                        continue
                    
                    # Download the file
                    print(f"Downloading {category} #{counts[category]}: {filename}...")
                    try:
                        client.download_media(message, file=file_path)
                        print(f"Successfully downloaded: {filename}")
                        total_count += 1
                    except Exception as e:
                        print(f"Error downloading {filename}: {e}")
        
        # Print summary
        if total_count == 0:
            print("No media files found in this channel.")
        else:
            print(f"\nDownload Summary:")
            print("-" * 40)
            for category, count in counts.items():
                if count > 0:
                    print(f"{category.capitalize()}: {count} files")
            print("-" * 40)
            print(f"Total: {total_count} files")
            print(f"Files saved to: {channel_dir}")
            
    except RPCError as e:
        print(f"A Telegram API error occurred: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        import traceback
        traceback.print_exc()

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Telegram Channel Media Downloader')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--lc', '--listchannels', action='store_true', help='List all channels')
    group.add_argument('--d', '--download', metavar='CHANNEL_ID', help='Download media from channel ID')
    group.add_argument('--reset-config', action='store_true', help='Reset API configuration')
    
    parser.add_argument('--limit', type=int, help='Limit number of messages to check')
    parser.add_argument('--dir', help='Download directory (default: downloaded_media)')
    parser.add_argument('--type', choices=['all', 'videos', 'images', 'documents', 'audio', 'archives'], 
                        default='all', help='Type of media to download (default: all)')
    
    args = parser.parse_args()
    
    # Reset config if requested
    if args.reset_config:
        config_path = Path.home() / '.teleripper' / 'config.ini'
        if config_path.exists():
            confirm = input("Are you sure you want to reset your API credentials? (y/n): ")
            if confirm.lower() in ['y', 'yes']:
                os.remove(config_path)
                print("Configuration reset. You'll be prompted for API credentials on next run.")
            else:
                print("Reset cancelled.")
            return
        else:
            print("No configuration file found. Nothing to reset.")
    
    # Get API credentials
    api_id, api_hash, session_name = create_config_if_not_exists()
    
    # Convert api_id to integer
    try:
        api_id = int(api_id)
    except ValueError:
        print("Error: API ID must be a number. Please reset configuration with --reset-config")
        return
    
    # Create client
    try:
        with TelegramClient(session_name, api_id, api_hash) as client:
            # Handle actions based on arguments
            if args.lc:
                list_channels(client)
            elif args.d:
                download_media(
                    client, 
                    args.d, 
                    download_dir=args.dir,
                    limit=args.limit,
                    media_types=[args.type]
                )
    except ConnectionError:
        print("Error: Could not connect to Telegram. Please check your internet connection.")
    except RPCError as e:
        print(f"A Telegram API error occurred: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
