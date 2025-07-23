#!/usr/bin/env python3
"""
🔧 UNICODE ENCODING FIX
=======================

Script để fix tất cả Unicode encoding issues trong codebase.
Thay thế emojis với text equivalents để tránh UnicodeEncodeError trên Windows console.

Root cause: Windows console (cmd) sử dụng cp1252 encoding không support Unicode emojis.
"""

import os
import re
import sys
from pathlib import Path

# Emoji mappings to text equivalents
EMOJI_REPLACEMENTS = {
    # Success/OK indicators
    '✅': '[OK]',
    '🎉': '[SUCCESS]',
    '💚': '[SUCCESS]',
    
    # Warning indicators  
    '⚠️': '[WARNING]',
    '🚨': '[ERROR]',
    
    # Tool/device indicators
    '🎙️': '[MIC]',
    '🎚️': '[AUDIO]',
    '🔧': '[TOOL]',
    '⚙️': '[CONFIG]',
    '🎯': '[TARGET]',
    '📊': '[STATS]',
    '📈': '[METRICS]',
    '📉': '[METRICS]',
    '💻': '[PC]',
    '🖥️': '[PC]',
    '📱': '[MOBILE]',
    '🎵': '[MUSIC]',
    '🎶': '[MUSIC]',
    '🔊': '[SOUND]',
    '🔇': '[MUTE]',
    '📢': '[SPEAKER]',
    '📣': '[SPEAKER]',
    
    # Status indicators
    '🟢': '[ON]',
    '🔴': '[OFF]',
    '🟡': '[PENDING]',
    '🟠': '[WARNING]',
    '⭐': '[STAR]',
    '✨': '[SPARKLE]',
    '💎': '[PREMIUM]',
    '🔥': '[HOT]',
    '❄️': '[COLD]',
    '⚡': '[FAST]',
    '🐌': '[SLOW]',
    '🚀': '[ROCKET]',
    '🎮': '[GAME]',
    
    # File/folder indicators
    '📁': '[FOLDER]',
    '📂': '[FOLDER]',
    '📄': '[FILE]',
    '📋': '[CLIPBOARD]',
    '📝': '[EDIT]',
    '✏️': '[EDIT]',
    '🗑️': '[DELETE]',
    '🗃️': '[ARCHIVE]',
    
    # Action indicators
    '🔄': '[REFRESH]',
    '🔃': '[REFRESH]',
    '🔁': '[REPEAT]',
    '⏪': '[REWIND]',
    '⏩': '[FORWARD]',
    '⏸️': '[PAUSE]',
    '⏹️': '[STOP]',
    '▶️': '[PLAY]',
    '🎬': '[ACTION]',
    
    # Other common emojis
    '🌟': '[STAR]',
    '🎨': '[ART]',
    '🧪': '[TEST]',
    '🔬': '[ANALYZE]',
    '🧩': '[PUZZLE]',
    '🎲': '[RANDOM]',
    '🎪': '[CIRCUS]',
    '🎭': '[THEATER]',
    '🎨': '[PAINT]',
    '🖌️': '[BRUSH]',
    '🖍️': '[CRAYON]',
    '📐': '[RULER]',
    '📏': '[RULER]',
    '🔍': '[SEARCH]',
    '🔎': '[SEARCH]',
    '🧹': '[CLEAN]',
    '🗒️': '[NOTE]',
    '📒': '[NOTEBOOK]',
    '📓': '[NOTEBOOK]',
    '📔': '[NOTEBOOK]',
    '📕': '[BOOK]',
    '📖': '[BOOK]',
    '📗': '[BOOK]',
    '📘': '[BOOK]',
    '📙': '[BOOK]',
    '📚': '[BOOKS]',
    '🎯': '[TARGET]',
    '🏆': '[TROPHY]',
    '🥇': '[GOLD]',
    '🥈': '[SILVER]',
    '🥉': '[BRONZE]',
    '🏅': '[MEDAL]',
    '🎖️': '[MEDAL]',
    '🏵️': '[ROSETTE]',
    '🎀': '[RIBBON]',
    '🎁': '[GIFT]',
    '🎊': '[CONFETTI]',
    '🎈': '[BALLOON]',
    '🎂': '[CAKE]',
    '🍰': '[CAKE]',
    '🧁': '[CUPCAKE]',
    '🍪': '[COOKIE]',
    '🍫': '[CHOCOLATE]',
    '🍭': '[LOLLIPOP]',
    '🍬': '[CANDY]',
    '🍩': '[DONUT]',
    '🍯': '[HONEY]',
    '🥧': '[PIE]',
    '🍎': '[APPLE]',
    '🍊': '[ORANGE]',
    '🍋': '[LEMON]',
    '🍌': '[BANANA]',
    '🍉': '[WATERMELON]',
    '🍇': '[GRAPES]',
    '🍓': '[STRAWBERRY]',
    '🫐': '[BLUEBERRY]',
    '🍈': '[MELON]',
    '🍒': '[CHERRY]',
    '🍑': '[PEACH]',
    '🥭': '[MANGO]',
    '🍍': '[PINEAPPLE]',
    '🥥': '[COCONUT]',
    '🥝': '[KIWI]',
    '🍅': '[TOMATO]',
    '🍆': '[EGGPLANT]',
    '🥑': '[AVOCADO]',
    '🥦': '[BROCCOLI]',
    '🥬': '[LETTUCE]',
    '🥒': '[CUCUMBER]',
    '🌶️': '[PEPPER]',
    '🫑': '[PEPPER]',
    '🌽': '[CORN]',
    '🥕': '[CARROT]',
    '🫒': '[OLIVE]',
    '🧄': '[GARLIC]',
    '🧅': '[ONION]',
    '🍄': '[MUSHROOM]',
    '🥔': '[POTATO]',
    '🍠': '[SWEET_POTATO]',
    '🥐': '[CROISSANT]',
    '🥖': '[BREAD]',
    '🍞': '[BREAD]',
    '🥨': '[PRETZEL]',
    '🥯': '[BAGEL]',
    '🧀': '[CHEESE]',
    '🥚': '[EGG]',
    '🍳': '[COOKING]',
    '🧈': '[BUTTER]',
    '🥞': '[PANCAKES]',
    '🧇': '[WAFFLE]',
    '🥓': '[BACON]',
    '🍗': '[CHICKEN]',
    '🍖': '[MEAT]',
    '🌭': '[HOT_DOG]',
    '🍔': '[BURGER]',
    '🍟': '[FRIES]',
    '🍕': '[PIZZA]',
    '🥪': '[SANDWICH]',
    '🥙': '[WRAP]',
    '🧆': '[FALAFEL]',
    '🌮': '[TACO]',
    '🌯': '[BURRITO]',
    '🥗': '[SALAD]',
    '🥘': '[PAELLA]',
    '🫕': '[FONDUE]',
    '🍝': '[PASTA]',
    '🍜': '[RAMEN]',
    '🍲': '[STEW]',
    '🍛': '[CURRY]',
    '🍣': '[SUSHI]',
    '🍱': '[BENTO]',
    '🥟': '[DUMPLING]',
    '🦪': '[OYSTER]',
    '🍤': '[SHRIMP]',
    '🍙': '[RICE_BALL]',
    '🍘': '[RICE_CRACKER]',
    '🍥': '[FISH_CAKE]',
    '🥠': '[FORTUNE_COOKIE]',
    '🥮': '[MOON_CAKE]',
    '🍢': '[SKEWER]',
    '🍡': '[DANGO]',
    '🍧': '[SHAVED_ICE]',
    '🍨': '[ICE_CREAM]',
    '🍦': '[SOFT_ICE_CREAM]',
    '🥧': '[PIE]',
    '🧊': '[ICE]',
    '🥤': '[CUP]',
    '🧃': '[JUICE_BOX]',
    '🧉': '[MATE]',
    '🧋': '[BUBBLE_TEA]',
    '🍼': '[BOTTLE]',
    '🍵': '[TEA]',
    '☕': '[COFFEE]',
    '🫖': '[TEAPOT]',
    '🍶': '[SAKE]',
    '🍾': '[CHAMPAGNE]',
    '🍷': '[WINE]',
    '🍸': '[COCKTAIL]',
    '🍹': '[TROPICAL_DRINK]',
    '🍺': '[BEER]',
    '🍻': '[CHEERS]',
    '🥂': '[CHAMPAGNE_GLASSES]',
    '🥃': '[WHISKEY]',
    '🫗': '[POURING]',
    
    # Generic fallbacks for any remaining emojis
    '🤖': '[BOT]',
    '👤': '[USER]',
    '👥': '[USERS]',
    '💡': '[IDEA]',
    '❤️': '[HEART]',
    '💙': '[HEART]',
    '💚': '[HEART]',
    '💛': '[HEART]',
    '🧡': '[HEART]',
    '💜': '[HEART]',
    '🖤': '[HEART]',
    '🤍': '[HEART]',
    '🤎': '[HEART]',
    '💔': '[BROKEN_HEART]',
    '💕': '[HEARTS]',
    '💖': '[HEARTS]',
    '💗': '[HEARTS]',
    '💘': '[HEARTS]',
    '💝': '[HEARTS]',
    '💞': '[HEARTS]',
    '💟': '[HEARTS]',
    '💠': '[DIAMOND]',
    '💯': '[100]',
    
    # Multi-character emojis (with variation selectors)
    '⚠️': '[WARNING]',
    '⚙️': '[CONFIG]',
    '🎙️': '[MIC]',
    '🎚️': '[AUDIO]',
    '🖥️': '[PC]',
    '🖌️': '[BRUSH]',
    '🖍️': '[CRAYON]',
    '✏️': '[EDIT]',
    '🗑️': '[DELETE]',
    '🗃️': '[ARCHIVE]',
    '🗒️': '[NOTE]',
    '⏸️': '[PAUSE]',
    '⏹️': '[STOP]',
    '▶️': '[PLAY]',
    '❄️': '[COLD]',
    '⚡': '[FAST]',
    '🔧': '[TOOL]',
}

def fix_unicode_in_file(file_path):
    """Fix unicode issues in a single file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Count replacements
        replacements_made = 0
        original_content = content
        
        # Replace emojis with text equivalents
        for emoji, replacement in EMOJI_REPLACEMENTS.items():
            if emoji in content:
                content = content.replace(emoji, replacement)
                replacements_made += 1
        
        # Additional regex-based fixes for any remaining unicode symbols
        # Remove variation selectors (U+FE0F)
        content = re.sub(r'\uFE0F', '', content)
        
        # Replace any remaining emoji-like characters with generic placeholder
        # This regex matches most Unicode emoji ranges
        emoji_pattern = re.compile(
            r'[\U0001F600-\U0001F64F]|'  # emoticons
            r'[\U0001F300-\U0001F5FF]|'  # symbols & pictographs
            r'[\U0001F680-\U0001F6FF]|'  # transport & map symbols
            r'[\U0001F1E0-\U0001F1FF]|'  # flags (iOS)
            r'[\U00002702-\U000027B0]|'  # dingbats
            r'[\U000024C2-\U0001F251]'   # enclosed characters
        )
        
        remaining_emojis = emoji_pattern.findall(content)
        if remaining_emojis:
            content = emoji_pattern.sub('[EMOJI]', content)
            replacements_made += len(remaining_emojis)
        
        # Write back if changes were made
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return replacements_made
        
        return 0
        
    except Exception as e:
        print(f"[ERROR] Failed to process {file_path}: {e}")
        return 0

def find_python_files(src_dir):
    """Find all Python files in src directory"""
    python_files = []
    for root, dirs, files in os.walk(src_dir):
        for file in files:
            if file.endswith('.py'):
                python_files.append(os.path.join(root, file))
    return python_files

def main():
    """Main fix function"""
    print("UNICODE ENCODING FIX - Starting...")
    
    src_dir = os.path.join(os.getcwd(), 'src')
    if not os.path.exists(src_dir):
        print(f"[ERROR] Source directory not found: {src_dir}")
        return
    
    # Find all Python files
    python_files = find_python_files(src_dir)
    print(f"[INFO] Found {len(python_files)} Python files to check")
    
    total_replacements = 0
    files_modified = 0
    
    # Process each file
    for file_path in python_files:
        rel_path = os.path.relpath(file_path, src_dir)
        replacements = fix_unicode_in_file(file_path)
        
        if replacements > 0:
            print(f"[FIXED] {rel_path}: {replacements} replacements")
            total_replacements += replacements
            files_modified += 1
        else:
            print(f"[OK] {rel_path}: no changes needed")
    
    print(f"\n[SUMMARY]")
    print(f"Files processed: {len(python_files)}")
    print(f"Files modified: {files_modified}")
    print(f"Total replacements: {total_replacements}")
    
    if files_modified > 0:
        print(f"\n[SUCCESS] Unicode encoding issues fixed!")
        print(f"You can now run the TTS workflow without UnicodeEncodeError.")
    else:
        print(f"\n[INFO] No unicode issues found.")

if __name__ == "__main__":
    main()