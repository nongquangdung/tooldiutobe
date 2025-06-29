#!/usr/bin/env python3
"""
🎭 94 UNIQUE EMOTION PROMPTS FOR VOICE STUDIO
============================================

Danh sách 94 đoạn văn độc đáo và diverse để preview emotions tốt hơn.
Mỗi emotion có prompt riêng biệt, sống động và thể hiện đúng cảm xúc.
"""

# 🎭 94 UNIQUE EMOTION PROMPTS - Diverse, engaging texts for each emotion
EMOTION_PROMPTS = {
    # === NEUTRAL & BASIC EMOTIONS ===
    "neutral": "The quarterly performance metrics indicate steady growth across all operational divisions, with projected improvements in efficiency over the next fiscal period.",
    "calm": "Listen to the gentle rhythm of rain against the window. Everything unfolds exactly as it should, in perfect harmony with the natural flow of time.",
    "happy": "Sunlight streams through the trees as laughter fills the air! This moment sparkles with pure joy, painting the world in vibrant, beautiful colors.",
    "sad": "Empty rooms echo with memories of what once was. The silence speaks volumes about dreams that drifted away like autumn leaves on the wind.",
    "angry": "This betrayal burns like fire in my chest! How dare you break your promises and disrespect everything we built together? I will not stand for this!",
    "surprised": "No way! Did that really just happen? My mind is completely blown—I never imagined such an incredible twist could be possible!",
    
    # === POSITIVE EMOTIONS ===
    "excited": "Adventure awaits beyond that horizon! Every fiber of my being vibrates with anticipation as we stand on the edge of something extraordinary and life-changing!",
    "cheerful": "What a glorious morning to embrace new possibilities! The birds are singing, flowers are blooming, and my heart overflows with optimism for today's adventures!",
    "optimistic": "Every challenge holds the seeds of opportunity within it. No matter how dark the clouds appear, I know sunshine will break through eventually.",
    "proud": "Years of dedication have culminated in this magnificent achievement! The countless hours of effort were worth every sacrifice to reach this pinnacle of success.",
    "grateful": "Your unwavering support lifted me when I was drowning in doubt. I am deeply moved by your kindness and will treasure this gift forever.",
    "delighted": "This exceeds every expectation I dared to have! The attention to detail, the craftsmanship, the sheer beauty—it's absolutely perfect in every way.",
    "enthusiastic": "This project ignites my imagination like fireworks! I can envision endless possibilities spreading before us like an ocean of creative potential.",
    "impressed": "Your mastery of this complex skill leaves me speechless. The precision, the artistry, the innovation—it's truly world-class excellence in action.",
    "praising": "The elegance with which you handled that crisis was extraordinary. Your leadership transformed chaos into triumph through pure wisdom and grace.",
    "amazed": "Reality seems to bend around this incredible phenomenon! What I'm witnessing defies everything I thought I understood about the laws of nature.",
    "stunned": "Words fail me completely. This revelation shatters my understanding of everything, leaving me breathless and searching for new comprehension.",
    "shocked": "This news hits like lightning from a clear sky! The implications are staggering, and I need time to process this earth-shattering information.",
    
    # === NEGATIVE EMOTIONS ===
    "disappointed": "The bitter taste of broken promises lingers in my heart. After placing my trust so completely, this outcome feels like a crushing blow.",
    "frustrated": "Every solution I attempt crumbles like sand through my fingers! This endless cycle of setbacks tests the very limits of my patience.",
    "irritated": "That incessant noise grates against my nerves like chalk on a blackboard! Please, for the love of peace, make it stop immediately!",
    "furious": "This flagrant violation of our agreement ignites a rage that burns hotter than molten steel! Your betrayal is absolutely inexcusable!",
    "disgusted": "The repulsive nature of this behavior turns my stomach. How anyone could stoop to such vile, deplorable actions is beyond my comprehension.",
    "hurt": "Those cruel words pierce my soul like daggers of ice. The pain cuts so deep that I wonder if this wound will ever truly heal.",
    "melancholy": "Autumn whispers stories of endings, painting the world in sepia tones of gentle sorrow. There's strange beauty in this bittersweet longing.",
    "melancholic": "The ghost of what might have been haunts these quiet moments. I drift through memories like shadows dancing in twilight's embrace.",
    
    # === DRAMATIC EMOTIONS ===
    "dramatic": "The curtain rises on the final scene! All of history has led to this pivotal moment where heroes are born and legends are written!",
    "passionate": "This burning desire consumes my very essence! I would brave the fires of hell itself to defend what sets my spirit ablaze!",
    "intense": "The air crackles with electricity as cosmic forces align! This moment pulses with the raw power to reshape destiny itself!",
    "commanding": "Hear me clearly, for I speak with absolute authority! Your compliance is not requested—it is demanded without question or hesitation!",
    "dominant": "I stand as the undisputed master of this domain! All decisions flow through my will, and all power bends to my command!",
    "demanding": "Results, not excuses! I require immediate action on all fronts. The time for deliberation has passed—now we execute with precision!",
    "stern": "Your conduct falls far below acceptable standards! This is your final warning before facing serious consequences for your actions.",
    "firm": "My decision stands like bedrock—unmovable and final! No amount of persuasion will alter this carefully considered judgment.",
    "assertive": "Let me be perfectly clear about my expectations. These standards are non-negotiable, and adherence is absolutely mandatory.",
    
    # === URGENT & WARNING EMOTIONS ===
    "urgent": "Time slips away like sand in an hourglass! Every precious second lost brings us closer to irreversible catastrophe!",
    "emergency": "Code red alert across all sectors! Drop everything and respond to this critical threat that demands immediate full attention!",
    "warning": "Halt your advance immediately! The path ahead conceals dangers that could prove fatal if you proceed without proper caution!",
    "alarm": "Sirens wail through the corridors of danger! All personnel must respond to this unprecedented crisis without delay!",
    "critical": "We balance on a razor's edge between triumph and disaster! One misstep now could topple everything we've fought to build!",
    "ominous": "Storm clouds gather with malevolent intent while ancient curses stir in the shadows. Something wicked approaches on silent wings.",
    "eerie": "Ghostly whispers drift through abandoned halls where shadows move without owners. The very walls seem to pulse with supernatural dread.",
    
    # === FEARFUL EMOTIONS ===
    "fearful": "Invisible threats lurk behind every corner, making my skin crawl with premonition! Something evil watches from the darkness beyond sight.",
    "anxious": "My heart pounds like thunder while scenarios of doom spiral through my racing mind! What if everything collapses into chaos?",
    "worried": "Sleep eludes me as nightmarish possibilities parade through my thoughts! The weight of uncertainty presses down like crushing stone.",
    "nervous": "Trembling hands betray my inner turmoil as sweat beads on my furrowed brow! This crucial moment tests every fiber of my being!",
    "restless": "Kinetic energy courses through my veins like electricity! I must move, must act, must channel this overwhelming force into motion!",
    "paranoid": "They conspire in whispered conferences, plotting my downfall! Every glance carries hidden meaning, every smile masks sinister intent!",
    "terrified": "Bone-deep terror freezes my blood as primal fear overwhelms all rational thought! This nightmare surpasses my darkest imaginings!",
    "horrified": "The abomination before me violates every law of nature and decency! My mind recoils from this vision of pure evil!",
    "fear": "Ancient instincts scream warnings as supernatural dread seeps into my soul! This place reeks of malevolent, otherworldly presence!",
    
    # === SARCASTIC & MOCKING EMOTIONS ===
    "sarcastic": "Oh, what a *revolutionary* idea! I'm sure nobody has ever attempted such a *brilliant* strategy in the entire history of civilization.",
    "mocking": "Behold the great mastermind in action! Such *impressive* intellect surely deserves a standing ovation for this *groundbreaking* achievement.",
    "ironic": "How perfectly fitting that the champion of truth becomes the master of deception! Life's sense of humor never ceases to amaze me.",
    "cynical": "Another politician promises paradise while picking our pockets. How refreshingly *original* and completely *trustworthy* they appear.",
    
    # === CONFUSED & UNCERTAIN EMOTIONS ===
    "confused": "These puzzle pieces refuse to form any coherent picture! My understanding crumbles like a house of cards in a hurricane!",
    "bewildered": "Reality shifted when I wasn't looking! This bizarre situation defies all logic and leaves me utterly disoriented!",
    "perplexed": "This enigma tangles my thoughts in knots! The more I analyze, the deeper the mystery becomes and the less I comprehend!",
    "puzzled": "The narrative fragments don't align to create any sensible story! Critical information remains hidden in impenetrable shadows!",
    "doubtful": "Skepticism clouds my judgment like morning fog! Something about this situation rings false, though I cannot pinpoint the deception!",
    "uncertain": "Multiple paths diverge before me, each shrouded in equal mystery! The compass of my decision-making spins wildly without direction!",
    "hesitant": "Caution whispers warnings while opportunity calls! Perhaps wisdom suggests we pause before leaping into this unknown abyss!",
    
    # === INNOCENT & CHILDLIKE EMOTIONS ===
    "innocent": "I never intended any harm—honest! My actions came from pure intentions, though the results surprised even me completely!",
    "naive": "But surely goodness lives in everyone's heart! Why would anyone choose cruelty when kindness feels so much more natural?",
    "childlike": "Let's build castles from pillows and blankets! Our imagination can transform this ordinary room into a magical kingdom of wonder!",
    
    # === MYSTERIOUS & ETHEREAL EMOTIONS ===
    "mysterious": "Ancient secrets whisper through moonlit corridors where forbidden knowledge sleeps! Some truths carry prices that mortals cannot afford to pay.",
    "mystical": "Sacred energies flow through crystalline streams of consciousness! The veil between worlds grows gossamer-thin in this enchanted realm.",
    "ethereal": "Starlight weaves melodies through dreams while celestial forces dance! Reality becomes fluid poetry written in languages of pure light.",
    "cryptic": "The key lies hidden within the riddle itself! Only those who see beyond surface illusions will unlock the treasure within!",
    "hypnotic": "Consciousness drifts on currents of amber honey while time dissolves into spirals of infinite possibility and transcendent peace.",
    "dreamy": "Cotton candy clouds carry wishes to sleeping mountains while rainbow bridges span oceans of liquid silver starlight.",
    
    # === ROMANTIC & SEDUCTIVE EMOTIONS ===
    "romantic": "Beneath this tapestry of stars, your presence transforms ordinary moments into eternal symphonies of perfect, breathtaking love.",
    "seductive": "Move closer, my darling, and let me share secrets that will ignite flames of desire in the depths of your beautiful soul.",
    "flirtatious": "Those sparkling eyes could melt the resolve of saints! You wield charm like a weapon designed to capture hearts completely.",
    
    # === FRIENDLY & SOCIAL EMOTIONS ===
    "friendly": "What a delightful surprise to encounter you here! Your radiant smile instantly brightens this ordinary day into something truly special!",
    "encouraging": "Your potential blazes like a beacon in the darkness! Trust in your abilities—greatness flows through your very essence!",
    "soft": "Rest now in this sanctuary of peace. Let healing warmth surround you while tomorrow's hopes gather strength in gentle silence.",
    
    # === SLEEPY & TIRED EMOTIONS ===
    "sleepy": "Velvet pillows beckon while drowsiness wraps around me like silk! These heavy eyelids surrender to the sweet embrace of slumber.",
    
    # === CONTEMPLATIVE EMOTIONS ===
    "contemplative": "Time weaves intricate patterns through the tapestry of choice and consequence! Each decision ripples through eternity's vast ocean.",
    
    # === HUMOROUS EMOTIONS ===
    "humorous": "Picture this absurd scene: me, conducting an important business meeting while wearing bunny slippers! Life's comedy writes itself beautifully!",
    "playful": "Adventure calls from the playground of imagination! Let's race clouds across the sky and chase butterflies through fields of laughter!",
    
    # === DESPERATE & PLEADING EMOTIONS ===
    "desperate": "All hope seems lost as options disappear like mirages! I reach out to you as my final lifeline in this ocean of despair!",
    "begging": "I cast away all pride to plead for your mercy! Please don't abandon me to face this darkness alone—I need you desperately!",
    "pleading": "From the depths of my heart, I implore your compassion! Consider the countless souls depending on your merciful decision!",
    "earnest": "Every syllable carries the weight of absolute truth! These words flow from my soul's deepest wells of sincere conviction!",
    
    # === SHY & EMBARRASSED EMOTIONS ===
    "shy": "Words tangle on my tongue like shy butterflies! Your presence makes my heart flutter with nervous, wonderful anticipation!",
    "embarrassed": "Crimson heat floods my cheeks as mortification overwhelms! Could the earth please open and swallow me whole right now?",
    
    # === INFORMATIVE & MATTER-OF-FACT ===
    "matter_of_fact": "Statistical analysis reveals definitive correlations between variables X and Y, supporting our hypothesis with 95% confidence intervals.",
    "informative": "Understanding requires mastering these fundamental principles: first establish parameters, then introduce controlled variables systematically.",
    
    # === WHISPER & SUSPENSEFUL ===
    "whisper": "Lean closer—walls have ears in this place! The secret I'm about to share could change everything we thought we knew!",
    "suspenseful": "Footsteps echo down empty hallways while shadows dance with sinister intent! Something approaches through the suffocating darkness!",
    
    # === ADDITIONAL EMOTIONS ===
    "admiring": "This masterpiece transcends mere craftsmanship to touch the divine! Every brushstroke sings with passion and technical brilliance beyond compare!",
    "cold": "Your apologies fall on deaf ears like snow on frozen ground. This bridge burned beyond repair the moment you chose betrayal over loyalty.",
    "contemptuous": "Is this pathetic display truly your finest effort? Such mediocrity insults the very concept of excellence and achievement!",
    "persuasive": "Envision the golden opportunities stretching endlessly before us! This chance may never return—seize destiny while fortune smiles upon us!",
    "confident": "Success flows through my veins like liquid courage! I've prepared for this moment and nothing can shake my unwavering self-assurance!",
    "admiring": "This artistry transcends human limitation to touch the divine! Every element harmonizes in perfect symphonic brilliance beyond mere mortal achievement!"
}

def update_emotion_config_tab_prompts():
    """
    Update Emotion Config Tab với 94 unique prompts
    """
    import os
    import re
    
    emotion_config_path = "src/ui/emotion_config_tab.py"
    
    if not os.path.exists(emotion_config_path):
        print(f"❌ File không tồn tại: {emotion_config_path}")
        return False
    
    # Read current file
    with open(emotion_config_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Pattern để tìm EMOTION_PROMPTS dictionary
    pattern = r'(EMOTION_PROMPTS\s*=\s*\{)[^}]+(\})'
    
    # Create new prompts string
    prompts_str = "EMOTION_PROMPTS = {\n"
    for emotion, prompt in EMOTION_PROMPTS.items():
        prompts_str += f'        "{emotion}": "{prompt}",\n'
    prompts_str = prompts_str.rstrip(',\n') + '\n    }'
    
    # Replace old prompts with new ones
    new_content = re.sub(pattern, prompts_str, content, flags=re.DOTALL)
    
    # Write updated file
    with open(emotion_config_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"✅ Đã update {len(EMOTION_PROMPTS)} unique prompts trong {emotion_config_path}")
    return True

if __name__ == "__main__":
    print("🎭 94 UNIQUE EMOTION PROMPTS FOR VOICE STUDIO")
    print("=" * 50)
    print(f"Total prompts: {len(EMOTION_PROMPTS)}")
    
    # Show sample prompts
    print("\n📝 Sample prompts:")
    sample_emotions = list(EMOTION_PROMPTS.keys())[:5]
    for emotion in sample_emotions:
        print(f"  {emotion}: {EMOTION_PROMPTS[emotion][:80]}...")
    
    # Update emotion config tab
    print("\n🔄 Updating emotion config tab...")
    if update_emotion_config_tab_prompts():
        print("✅ Successfully updated emotion config tab with unique prompts!")
    else:
        print("❌ Failed to update emotion config tab") 