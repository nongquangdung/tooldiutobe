#!/usr/bin/env python3
"""
🎭 CREATE 95 UNIQUE EMOTION PROMPTS
==================================

Script tạo 95 đoạn văn độc đáo cho mỗi emotion để preview nghe khác biệt.
Thay vì "This is a test" cho tất cả, mỗi emotion sẽ có prompt riêng.
"""

import json
import re
import os

# 🎭 95 UNIQUE EMOTION PROMPTS - Diverse, engaging texts for each emotion
UNIQUE_PROMPTS = {
    # === NEUTRAL CATEGORY ===
    "neutral": "The quarterly performance report indicates steady progress across all operational divisions, with projected efficiency improvements anticipated for the upcoming fiscal period.",
    "calm": "Listen to the gentle rhythm of raindrops against the window. Everything unfolds exactly as it should, in perfect harmony with nature's peaceful flow.",
    "contemplative": "Time weaves intricate patterns through the tapestry of choice and consequence. Each decision creates ripples that echo through eternity's vast ocean.",
    "soft": "Rest now in this sanctuary of tranquil peace. Let healing warmth surround you while tomorrow's gentle hopes gather strength in comforting silence.",
    "whisper": "Lean closer—these walls have sensitive ears. The secret I'm about to share could change everything we thought we understood about reality.",
    "matter_of_fact": "Statistical analysis reveals definitive correlations between variables X and Y, supporting our research hypothesis with ninety-five percent confidence intervals.",
    "informative": "Understanding requires mastering these fundamental principles: first establish baseline parameters, then systematically introduce controlled experimental variables.",
    "sleepy": "Velvet pillows beckon while drowsiness wraps around me like warm silk. These heavy eyelids surrender to slumber's sweet, irresistible embrace.",
    
    # === POSITIVE CATEGORY ===
    "happy": "Sunlight streams through dancing leaves as laughter fills the crisp morning air! This magical moment sparkles with pure joy, painting our world in vibrant colors.",
    "excited": "Adventure awaits beyond that shimmering horizon! Every fiber of my being vibrates with anticipation as we stand on the edge of something extraordinary!",
    "cheerful": "What a glorious morning to embrace endless new possibilities! Birds are singing melodiously, flowers are blooming everywhere, and my heart overflows with optimism!",
    "friendly": "What a delightful surprise to encounter you here today! Your radiant smile instantly brightens this ordinary moment into something truly wonderful and special.",
    "confident": "Success flows through my veins like liquid courage and determination! I've prepared extensively for this moment and nothing can shake my unwavering self-assurance.",
    "encouraging": "Your incredible potential blazes like a beacon cutting through darkness! Trust completely in your amazing abilities—greatness flows naturally through your very essence.",
    "admiring": "This masterpiece transcends mere human craftsmanship to touch something truly divine! Every brushstroke sings with passion and technical brilliance beyond earthly comparison.",
    "optimistic": "Every challenging obstacle holds precious seeds of golden opportunity within it. No matter how dark these storm clouds appear, sunshine will break through.",
    "proud": "Years of unwavering dedication have culminated in this magnificent achievement! Those countless hours of effort were worth every sacrifice to reach this pinnacle.",
    "grateful": "Your unwavering support lifted me when I was drowning in overwhelming doubt. I am deeply moved by your kindness and will treasure this forever.",
    "delighted": "This exceeds every expectation I dared to have! The attention to detail, the exquisite craftsmanship, the sheer beauty—it's absolutely perfect in every way.",
    "enthusiastic": "This incredible project ignites my imagination like brilliant fireworks! I can envision endless possibilities spreading before us like an ocean of creative potential.",
    "impressed": "Your complete mastery of this complex skill leaves me absolutely speechless. The precision, the artistry, the innovation—it's truly world-class excellence in action.",
    "praising": "The elegant grace with which you handled that crisis was extraordinary. Your wise leadership transformed chaos into triumph through pure wisdom.",
    "amazed": "Reality itself seems to bend around this incredible phenomenon! What I'm witnessing defies everything I thought I understood about natural laws.",
    "playful": "Adventure calls from imagination's endless playground! Let's race fluffy white clouds across the azure sky and chase butterflies through fields of laughter!",
    "romantic": "Beneath this tapestry of twinkling stars, your presence transforms ordinary moments into eternal symphonies of perfect, breathtaking love and devotion.",
    
    # === NEGATIVE CATEGORY ===
    "sad": "Empty rooms echo with bittersweet memories of what once was. The profound silence speaks volumes about cherished dreams that drifted away like autumn leaves.",
    "angry": "This burning betrayal ignites like fire in my chest! How dare you break sacred promises and disrespect everything we built together? Unforgivable!",
    "sarcastic": "Oh, what a *revolutionary* masterpiece of genius! I'm absolutely certain nobody has ever attempted such a *brilliant* strategy in civilization's entire history.",
    "disappointed": "The bitter taste of broken promises lingers heavily in my heart. After placing my complete trust so willingly, this outcome feels devastatingly crushing.",
    "anxious": "My heart pounds like thunder while scenarios of doom spiral endlessly through my racing mind! What if everything collapses into complete chaos?",
    "frustrated": "Every solution I desperately attempt crumbles like sand through my fingers! This endless cycle of setbacks tests the very limits of my patience.",
    "hurt": "Those cruel words pierce my vulnerable soul like daggers of ice. The pain cuts so incredibly deep that I wonder if this wound will heal.",
    "melancholy": "Autumn whispers haunting stories of endings, painting the world in sepia tones of gentle sorrow. There's strange beauty in this bittersweet longing.",
    "melancholic": "The ghost of what might have been haunts these quiet moments. I drift through memories like shadows dancing in twilight's mysterious embrace.",
    "irritated": "That incessant noise grates against my nerves like chalk scraping on a blackboard! Please, for the love of peace, make it stop immediately!",
    "furious": "This flagrant violation of our sacred agreement ignites rage that burns hotter than molten steel! Your betrayal is absolutely inexcusable and unforgivable!",
    "disgusted": "The repulsive nature of this behavior turns my stomach completely. How anyone could stoop to such vile, deplorable actions is beyond comprehension.",
    "cold": "Your hollow apologies fall on deaf ears like snow on frozen ground. This bridge burned beyond repair the moment you chose betrayal over loyalty.",
    "contemptuous": "Is this pathetic display truly your finest effort? Such mediocrity insults the very concept of excellence and achievement in every possible way.",
    "suspicious": "Something doesn't feel right about this situation. Hidden motives lurk beneath the surface, and I can sense deception in every carefully chosen word.",
    "bitter": "Life's cruel irony leaves a metallic taste of disappointment. Years of hope have crystallized into this moment of crushing, inevitable disillusionment.",
    "gloomy": "Gray clouds mirror the weight pressing down on my weary spirit. Even sunshine seems unable to penetrate this thick blanket of despair.",
    "resentful": "Old wounds reopen with fresh pain, reminding me of every slight and injustice. Forgiveness feels impossible when betrayal runs this deep.",
    
    # === DRAMATIC CATEGORY ===
    "dramatic": "The curtain rises on the final scene! All of history has led to this pivotal moment where heroes are born and legends are written!",
    "mysterious": "Ancient secrets whisper through moonlit corridors where forbidden knowledge sleeps eternally! Some truths carry prices that mortals cannot afford to pay.",
    "surprised": "No way! Did that really just happen? My mind is completely blown—I never imagined such an incredible twist could possibly be real!",
    "urgent": "Time slips away like sand in an hourglass! Every precious second lost brings us closer to irreversible catastrophe and eternal regret!",
    "passionate": "This burning desire consumes my very essence! I would brave the fires of hell itself to defend what sets my spirit ablaze!",
    "intense": "The air crackles with electricity as cosmic forces align! This moment pulses with the raw power to reshape destiny itself!",
    "suspenseful": "Footsteps echo down empty hallways while shadows dance with sinister intent! Something approaches through the suffocating darkness, waiting to strike!",
    "ethereal": "Starlight weaves melodies through dreams while celestial forces dance! Reality becomes fluid poetry written in languages of pure, transcendent light.",
    
    # === AUTHORITATIVE CATEGORY ===
    "commanding": "Hear me clearly, for I speak with absolute authority! Your compliance is not requested—it is demanded without question or hesitation!",
    "dominant": "I stand as the undisputed master of this domain! All decisions flow through my will, and all power bends to my command!",
    "demanding": "Results, not excuses! I require immediate action on all fronts. The time for deliberation has passed—now we execute with precision!",
    "stern": "Your conduct falls far below acceptable standards! This is your final warning before facing serious consequences for your unacceptable actions.",
    "firm": "My decision stands like bedrock—unmovable and final! No amount of persuasion will alter this carefully considered judgment.",
    "assertive": "Let me be perfectly clear about my expectations. These standards are non-negotiable, and adherence is absolutely mandatory without exception.",
    
    # === SPECIAL CATEGORY ===
    "persuasive": "Envision the golden opportunities stretching endlessly before us! This chance may never return—seize destiny while fortune smiles upon us!",
    "humorous": "Picture this absurd scene: me, conducting an important business meeting while wearing bright pink bunny slippers! Life's comedy writes itself beautifully!",
    "flirtatious": "Those sparkling eyes could melt the resolve of saints! You wield charm like a weapon designed to capture hearts completely and effortlessly.",
    "shy": "Words tangle on my tongue like shy butterflies! Your presence makes my heart flutter with nervous, wonderful anticipation and sweet embarrassment.",
    "seductive": "Move closer, my darling, and let me share intimate secrets that will ignite flames of desire in the depths of your beautiful soul.",
    "innocent": "I never intended any harm—honest! My actions came from pure intentions, though the results surprised even me completely and unexpectedly.",
    "childlike": "Let's build magical castles from pillows and blankets! Our imagination can transform this ordinary room into a kingdom of wonder!",
    "naive": "But surely goodness lives in everyone's heart! Why would anyone choose cruelty when kindness feels so much more natural and beautiful?",
    "dreamy": "Cotton candy clouds carry wishes to sleeping mountains while rainbow bridges span oceans of liquid silver starlight and cosmic wonder.",
    "hypnotic": "Consciousness drifts on currents of amber honey while time dissolves into spirals of infinite possibility and transcendent, eternal peace.",
    
    # === SURPRISE CATEGORY ===
    "shocked": "This news hits like lightning from a perfectly clear sky! The implications are staggering, and I need time to process this earth-shattering information!",
    "stunned": "Words fail me completely and utterly. This revelation shatters my understanding of everything, leaving me breathless and searching for new comprehension.",
    "amazed": "Reality seems to bend around this incredible phenomenon! What I'm witnessing defies everything I thought I understood about the laws of nature.",
    
    # === DESPERATE CATEGORY ===
    "earnest": "Every syllable carries the weight of absolute truth! These words flow from my soul's deepest wells of sincere conviction and heartfelt honesty.",
    "desperate": "All hope seems lost as options disappear like mirages! I reach out to you as my final lifeline in this ocean of despair!",
    "begging": "I cast away all pride to plead for your mercy! Please don't abandon me to face this darkness alone—I need you desperately!",
    
    # === NERVOUS CATEGORY ===
    "worried": "Sleep eludes me as nightmarish possibilities parade through my thoughts! The weight of uncertainty presses down like crushing stone.",
    "nervous": "Trembling hands betray my inner turmoil as sweat beads on my furrowed brow! This crucial moment tests every fiber of my being!",
    "restless": "Kinetic energy courses through my veins like electricity! I must move, must act, must channel this overwhelming force into motion!",
    "paranoid": "They conspire in whispered conferences, plotting my downfall! Every glance carries hidden meaning, every smile masks sinister intent!",
    
    # === MYSTERIOUS CATEGORY ===
    "ominous": "Storm clouds gather with malevolent intent while ancient curses stir in the shadows. Something wicked approaches on silent wings.",
    "eerie": "Ghostly whispers drift through abandoned halls where shadows move without owners. The very walls seem to pulse with supernatural dread.",
    "cryptic": "The key lies hidden within the riddle itself! Only those who see beyond surface illusions will unlock the treasure within!",
    
    # === URGENT CATEGORY ===
    "warning": "Halt your advance immediately! The path ahead conceals dangers that could prove fatal if you proceed without proper caution!",
    "emergency": "Code red alert across all sectors! Drop everything and respond to this critical threat that demands immediate full attention!",
    "alarm": "Sirens wail through the corridors of danger! All personnel must respond to this unprecedented crisis without delay!",
    "critical": "We balance on a razor's edge between triumph and disaster! One misstep now could topple everything we've fought to build!",
    
    # === SARCASTIC CATEGORY ===
    "mocking": "Behold the great mastermind in action! Such *impressive* intellect surely deserves a standing ovation for this *groundbreaking* achievement.",
    "ironic": "How perfectly fitting that the champion of truth becomes the master of deception! Life's sense of humor never ceases to amaze me.",
    "cynical": "Another politician promises paradise while picking our pockets. How refreshingly *original* and completely *trustworthy* they appear.",
    
    # === CONFUSED CATEGORY ===
    "embarrassed": "Crimson heat floods my cheeks as mortification overwhelms! Could the earth please open and swallow me whole right now?",
    "hesitant": "Caution whispers warnings while opportunity calls! Perhaps wisdom suggests we pause before leaping into this unknown abyss!",
    "uncertain": "Multiple paths diverge before me, each shrouded in equal mystery! The compass of my decision-making spins wildly without direction!",
    "perplexed": "This enigma tangles my thoughts in knots! The more I analyze, the deeper the mystery becomes and the less I comprehend!",
    "doubtful": "Skepticism clouds my judgment like morning fog! Something about this situation rings false, though I cannot pinpoint the deception!",
    "confused": "These puzzle pieces refuse to form any coherent picture! My understanding crumbles like a house of cards in a hurricane!",
    
    # === INNOCENT CATEGORY ===
    "naive": "But surely goodness lives in everyone's heart! Why would anyone choose cruelty when kindness feels so much more natural?",
    "childlike": "Let's build castles from pillows and blankets! Our imagination can transform this ordinary room into a magical kingdom of wonder!",
    
    # === FEAR EMOTIONS ===
    "fearful": "Invisible threats lurk behind every corner, making my skin crawl with premonition! Something evil watches from the darkness beyond sight.",
    "terrified": "Bone-deep terror freezes my blood as primal fear overwhelms all rational thought! This nightmare surpasses my darkest imaginings!",
    "horrified": "The abomination before me violates every law of nature and decency! My mind recoils from this vision of pure evil!",
    "fear": "Ancient instincts scream warnings as supernatural dread seeps into my soul! This place reeks of malevolent, otherworldly presence!",
    
    # === ADDITIONAL EMOTIONS ===
    "bewildered": "Reality shifted when I wasn't looking! This bizarre situation defies all logic and leaves me utterly disoriented!",
    "puzzled": "The narrative fragments don't align to create any sensible story! Critical information remains hidden in impenetrable shadows!",
    "pleading": "From the depths of my heart, I implore your compassion! Consider the countless souls depending on your merciful decision!",
    "mystical": "Sacred energies flow through crystalline streams of consciousness! The veil between worlds grows gossamer-thin in this enchanted realm."
}

def update_emotion_config_tab():
    """Update emotion config tab với unique prompts"""
    
    # Đọc file hiện tại
    emotion_config_path = "src/ui/emotion_config_tab.py"
    
    if not os.path.exists(emotion_config_path):
        print(f"❌ File không tồn tại: {emotion_config_path}")
        return False
    
    print("📖 Đang đọc emotion config tab...")
    with open(emotion_config_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Tìm EMOTION_PROMPTS dictionary và thay thế
    # Pattern to match EMOTION_PROMPTS = { ... }
    pattern = r'(EMOTION_PROMPTS\s*=\s*\{)[^}]*(\})'
    
    # Tạo new prompts string
    prompts_lines = []
    for emotion, prompt in UNIQUE_PROMPTS.items():
        # Escape quotes
        escaped_prompt = prompt.replace('"', '\\"')
        prompts_lines.append(f'        "{emotion}": "{escaped_prompt}"')
    
    new_prompts_block = f"EMOTION_PROMPTS = {{\n" + ",\n".join(prompts_lines) + "\n    }"
    
    # Replace trong content
    import re
    new_content = re.sub(pattern, new_prompts_block, content, flags=re.DOTALL)
    
    # Write updated file
    print("✏️ Đang ghi file đã update...")
    with open(emotion_config_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    return True

def create_test_script():
    """Tạo test script để verify unique prompts"""
    test_content = '''#!/usr/bin/env python3
"""
🧪 TEST 95 UNIQUE EMOTION PROMPTS
================================
Test script để verify các unique prompts hoạt động
"""

import sys
sys.path.append('src')

from ui.emotion_config_tab import EmotionConfigTab
from core.unified_emotion_system import UnifiedEmotionSystem

def test_unique_prompts():
    print("🧪 Testing 95 unique emotion prompts...")
    
    # Load emotions
    system = UnifiedEmotionSystem()
    all_emotions = system.get_all_emotions()
    
    print(f"✅ Loaded {len(all_emotions)} emotions")
    
    # Test prompts
    from ui.emotion_config_tab import EMOTION_PROMPTS
    
    print(f"📝 Available prompts: {len(EMOTION_PROMPTS)}")
    
    # Check coverage
    emotions_with_prompts = 0
    for emotion_name in all_emotions.keys():
        if emotion_name in EMOTION_PROMPTS:
            emotions_with_prompts += 1
            prompt = EMOTION_PROMPTS[emotion_name]
            print(f"  ✅ {emotion_name}: {prompt[:50]}...")
        else:
            print(f"  ❌ {emotion_name}: NO UNIQUE PROMPT")
    
    print(f"\\n📊 Coverage: {emotions_with_prompts}/{len(all_emotions)} emotions")
    print(f"📊 Unique prompts: {len(set(EMOTION_PROMPTS.values()))}/{len(EMOTION_PROMPTS)}")
    
    if emotions_with_prompts == len(all_emotions):
        print("🎉 ALL EMOTIONS HAVE UNIQUE PROMPTS!")
    else:
        print("⚠️ Some emotions missing unique prompts")

if __name__ == "__main__":
    test_unique_prompts()
'''
    
    with open("test_95_unique_prompts.py", "w", encoding="utf-8") as f:
        f.write(test_content)
    
    print("✅ Đã tạo test_95_unique_prompts.py")

def main():
    print("🎭 CREATE 95 UNIQUE EMOTION PROMPTS")
    print("=" * 50)
    
    print(f"📊 Total unique prompts: {len(UNIQUE_PROMPTS)}")
    
    # Sample prompts
    print("\\n📝 Sample unique prompts:")
    samples = ["neutral", "excited", "mysterious", "sarcastic", "terrified"]
    for emotion in samples:
        if emotion in UNIQUE_PROMPTS:
            prompt = UNIQUE_PROMPTS[emotion][:60] + "..." if len(UNIQUE_PROMPTS[emotion]) > 60 else UNIQUE_PROMPTS[emotion]
            print(f"  • {emotion}: {prompt}")
    
    # Update emotion config tab
    print("\\n🔄 Updating emotion config tab...")
    if update_emotion_config_tab():
        print("✅ Successfully updated emotion config tab!")
    else:
        print("❌ Failed to update emotion config tab")
    
    # Create test script
    print("\\n🧪 Creating test script...")
    create_test_script()
    
    print("\\n🎉 HOÀN THÀNH!")
    print("\\n📋 HƯỚNG DẪN SỬ DỤNG:")
    print("1. Chạy: python test_95_unique_prompts.py để test")
    print("2. Mở Voice Studio > Emotion Config Tab")
    print("3. Preview bất kỳ emotion nào")
    print("4. Mỗi emotion giờ sẽ có đoạn văn riêng biệt!")
    print("5. Audio preview sẽ nghe khác biệt rõ rệt")

if __name__ == "__main__":
    main() 