# Video Factory - Project State Document

## Overview

Video Factory is an automated YouTube documentary production pipeline.

The goal is to generate complete faceless YouTube documentary videos from a single topic prompt with minimal manual intervention.

Current workflow:

Topic
→ AI script generation
→ AI image search generation
→ Wikimedia Commons image gathering
→ AI narration generation
→ Video rendering
→ Upload to YouTube

The project is specifically optimized around:

* Documentary content
* History content
* Sailing content
* Educational content
* Long-form YouTube videos

The system currently produces videos approximately 8-15 minutes long depending on script length.

---

# Current Architecture

## main.py

Acts as the orchestrator.

Current flow:

1. Ask for topic
2. Ask whether to generate a new script
3. Ask whether to generate new images
4. Ask whether to generate new voice
5. Build final video

This allows expensive generation steps to be skipped when testing.

Example:

Generate new script? (y/n)
Generate new images? (y/n)
Generate new voice? (y/n)

This dramatically reduces Gemini API usage.

---

# Script Generation

## script.py

Uses Gemini.

Current model:

gemini-2.5-flash-lite

Reason:

* Faster
* Higher RPM limits
* Lower rate limit pressure

Prompt style:

* Documentary narration
* 1500-2000 words minimum
* Conversational
* Retention-focused
* No narrator labels
* No markdown
* No visual cues
* No music cues
* No stage directions

Output must be pure spoken narration.

Goal:
Narration should sound like a real YouTube documentary channel.

---

# Image Search Generation

## searches.py

Uses Gemini.

Purpose:

Convert topic into a list of visual search terms.

Example:

Topic:
"The dangerous truth about cheap sailboats"

Outputs:

* Sailboat repair
* Abandoned sailboat
* Boat survey
* Marina haul out
* Marine diesel engine
* Boat graveyard
* Catalina 30
* Boat insurance
* etc.

These searches are used for Wikimedia image retrieval.

Current search count:
Approximately 15-20 searches.

---

# Wikimedia Image System

## images.py

Major rewrite completed.

Initial Wikimedia API implementation returned zero images.

Problem:
Commons search API is extremely inconsistent.

Current solution:

Search Wikimedia Commons page titles.

Then retrieve file metadata.

Then download image thumbnails.

---

# Major Discovery

Downloading full-resolution Wikimedia images results in:

HTTP 429
Too Many Requests

Wikimedia aggressively rate limits direct image downloads.

Solution:

Use thumbnail URLs instead.

Example:

BAD:

upload.wikimedia.org/...fullres.jpg

GOOD:

upload.wikimedia.org/.../thumb/.../1280px-image.jpg

This completely solved downloading.

---

# Current Image Pipeline

Gemini search terms
→ Wikimedia search
→ Retrieve file metadata
→ Build thumbnail URL
→ Download thumbnail
→ Save locally

Images stored in:

images/

---

# Image Problems Solved

Solved:

* Wikimedia returning zero results
* Broken image URLs
* 429 rate limits
* Invalid image downloads
* HTML error pages saved as JPGs

---

# Remaining Image Issues

Portrait images often create:

* Large black bars
* Weird framing

Currently acceptable.

Future improvement:

Detect aspect ratio and use different animation styles.

Example:

Landscape:
Slow zoom

Portrait:
Slow vertical pan

Ultra portrait:
Blurred background fill

---

# Voice Generation

## voice.py

Originally:

gTTS

Problems:

* Robotic
* Slow speaking rate
* Network dependency
* SSL issues
* Random failures

---

# Current Voice System

Piper TTS

Advantages:

* Local
* Free
* Fast
* No rate limits
* Better quality

Current status:

Working.

Voice quality significantly improved.

Narration stored in:

audio/narration.mp3

---

# Gemini API Issues Encountered

## Rate Limits

Hit repeatedly.

Free tier limits:

Gemini 2.5 Flash

5 RPM

20 requests/day

This caused:

* 503 errors
* temporary failures

Mitigation:

* Generate script only when needed
* Generate image searches only when needed
* Reuse outputs

---

## API Key Leak

A Gemini API key was hardcoded.

Google detected it.

Error:

403 PERMISSION_DENIED

"Your API key was reported as leaked."

Fix:

Move API keys to:

.env

Example:

GEMINI_API_KEY=xxxxx

Use:

python-dotenv

Never hardcode keys again.

---

# Video Rendering

## Original System

MoviePy

Worked.

Problems:

* Extremely slow
* Multi-hour render times
* High memory usage

---

# Current System

FFmpeg + NVENC

Major speed improvement.

Current pipeline:

Images
→ Individual clips
→ Concatenate clips
→ Add narration audio
→ Output final MP4

---

# Video Generation Flow

Image
→ Animated clip

Animated clips
→ video_only.mp4

video_only.mp4

* narration.mp3

→ final_video.mp4

---

# Current Resolution

Testing:
1920x1080

Production:
2560x1440

Reason:

Allows zooming without visible quality loss.

---

# Current Motion System

Status:

In active development.

---

## MoviePy Version

Used:

* Slow zoom
* Smooth transforms

Pros:

* Smooth

Cons:

* Extremely slow

---

## FFmpeg Zoompan Version

Pros:

* Fast

Cons:

* Jitter
* Drifting
* Portrait issues

Current conclusion:

zoompan is not ideal.

---

# Current Research Direction

Replace zoompan.

Possible future solution:

scale + crop

instead of

zoompan

Goal:

Maintain FFmpeg speed while achieving MoviePy smoothness.

---

# Git Lessons Learned

Generated files should NOT be committed.

Ignore:

output/
temp_clips/
images/
audio/

File types:

*.mp4
*.mp3
*.wav

Use:

.gitignore

---

# Current Channel Strategy

Content style:

Educational documentary

Target audience:

* Sailors
* Aspiring sailors
* Liveaboards
* Boat buyers
* General curiosity viewers

Example topics:

* The dangerous truth about cheap sailboats
* Why older sailboats are disappearing
* The hidden cost of free boats
* How insurance is killing affordable sailing
* The economics of marinas
* The future of cruising

---

# Future Features

## High Priority

Thumbnail generation

Potential approaches:

1. Gemini image prompts
2. Stable Diffusion
3. Flux
4. DALL-E
5. Manual generation

---

## High Priority

Improved motion engine

Goal:

Smooth documentary-style Ken Burns effect.

Without MoviePy render times.

---

## High Priority

Background music

Potential flow:

Narration
+
music ducking
+
final mix

---

## Medium Priority

Chapter generation

Output:

00:00 Intro

01:32 The Problem

03:54 Insurance

etc.

Useful for YouTube uploads.

---

## Medium Priority

Automatic descriptions

Generate:

* Title
* Description
* Tags

Alongside video.

---

## Medium Priority

Thumbnail text generation

Current workflow is manual.

Could be automated.

---

## Long-Term Vision

One prompt.

Example:

"The dangerous truth about cheap sailboats"

Produces:

* Full script
* Narration
* Images
* Thumbnail
* Title
* Description
* Tags
* Final video

With zero manual editing.

This is the ultimate project goal.
