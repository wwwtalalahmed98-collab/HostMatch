# HTGAA Final Project — AI-Assisted Synthetic Biology Proposal Generator

This repository contains a **Claude Code skill** that guides you through designing and writing a structured synthetic biology project proposal. The AI acts as a scientific design partner, helping you develop DNA constructs, automated lab workflows, and assay strategies — then generates a complete, submission-ready Markdown proposal.

---

## What This Does

The skill runs an interactive two-phase dialogue:

- **Phase 1 — Design:** The AI asks structured questions about your biological problem, DNA construct, assay strategy, and automation workflow. It does not write anything yet.
- **Phase 2 — Generation:** Once you say `generate proposal`, the AI writes a complete Markdown proposal to `projects/yourname_idea.md`, including GenBank sequences, plate layouts, hypothetical data, and a budget table with supplier links.

---

## Two Ways to Use This Skill

---

### Option A — Free (No Installation Required)

This works with a free [claude.ai](https://claude.ai) account. No subscription, no terminal, no setup.

**Steps:**

1. Go to [claude.ai](https://claude.ai) and sign in — Google sign-in is supported on the free tier.
2. Open `skills/SKILL.md` in any text editor and **copy the entire contents**.
3. Start a new Claude conversation and paste the contents with this message:

   > *Please follow the skill instructions below and begin Phase 1:*
   > [paste SKILL.md contents here]

4. Claude will read the skill and begin the project design dialogue immediately.
5. When you are ready, say `generate proposal` and copy the output into a new `.md` file in the `projects/` folder.

> **Tip:** If you want the conversation to persist across sessions, use the **Projects** feature on Claude.ai (available on free tier) — paste the SKILL.md contents into the Project Instructions field so it loads automatically every time.

---

### Option B — Claude Code CLI (Pro or Max Subscription)

This gives you a richer experience with automatic file saving, skill invocation via `/htgaa-final-project`, and the proposal written directly to `projects/`.

**Prerequisites:**

Install Claude Code (requires Node.js 18+):

```bash
npm install -g @anthropic-ai/claude-code
```

If Node.js is not installed, download it from [nodejs.org](https://nodejs.org) (choose the LTS version).

**Log in:**

```bash
claude
```

A browser window will open. Sign in with your Claude.ai account — Google sign-in is supported. Requires a **Claude Pro or Max subscription**.

---

## Setup (Option B — Claude Code only)

### 1. Get the Repository

```bash
git clone <repo-url>
cd htgaa-projects
```

Or unzip the folder if received as a zip file, then navigate into it.

### 2. Verify the Directory Structure

```
htgaa-projects/
├── README.md               ← you are here
├── skills/
│   └── SKILL.md            ← the skill definition (do not rename)
└── projects/               ← generated proposals appear here
```

### 3. Launch Claude Code

From inside the `htgaa-projects` directory:

```bash
claude
```

This is important — Claude Code must be launched from this folder so it can find the skill file.

---

## Using the Skill

### Option A — claude.ai (Free)

1. Open `skills/SKILL.md`, copy all contents.
2. Go to [claude.ai](https://claude.ai), start a new chat.
3. Paste with: *"Please follow the skill instructions below and begin Phase 1:"*
4. Work through the dialogue, then say `generate proposal`.
5. Copy the output into `projects/yourname_idea.md`.

### Option B — Claude Code CLI

In your Claude Code session, type:

```
/htgaa-final-project
```

The AI loads the skill and begins Phase 1. When ready:

```
generate proposal
```

The proposal is written automatically to `projects/yourname_idea.md`.

---

### Phase 1 — Answer the Questions

Whichever option you use, the AI will ask about:

- Your biological problem and organism/system
- DNA construct design (gene, promoter, reporters)
- Assay or screening strategy
- Automation workflow preferences
- Validation experiment

**You do not need to know everything upfront.** If you are unsure, say so — the AI will offer suggestions and help you brainstorm.

---

## Output Format

Each generated proposal includes:

| Section | Contents |
|---|---|
| Abstract | 150+ word summary |
| Project Aims | 3 aims (experimental, medium-term, visionary) |
| Background | Literature review, innovation, significance, bioethics |
| Experimental Design | 15+ steps with machines, plates, timelines, and a plate layout diagram |
| Techniques | Checklist + 2 expanded technique descriptions |
| Validation | Protocol, techniques used, hypothetical data with ASCII graph |
| Additional Info | References and budget table with supplier links |

The proposal also includes a **GenBank-format code block** for at least one DNA construct and **Twist Bioscience insert sequences** ready to paste into the ordering portal.

---

## Updating the Skill

The skill behaviour is entirely defined by `skills/SKILL.md`. To update prompting rules, add new equipment, change output requirements, or modify section structure, edit that file directly. Changes take effect the next time you invoke `/htgaa-final-project`.

---

## Tips for Students

- **Be specific early.** The more detail you give in Phase 1, the less back-and-forth is needed.
- **You can restart at any time.** Just say `let's start again` and the AI will re-read the skill and begin fresh.
- **You can ask for revisions.** After `generate proposal`, you can ask the AI to update any section (e.g. "can you add a western blot validation step?").
- **Prefer cell-free for Aim 1.** BL21(DE3) cell-free extract is available in the lab — this keeps your first aim technically realistic and avoids mammalian cell culture complexity.
- **The Twist order defaults to whole plasmid synthesis.** This is faster and requires no cloning. If your insert is >5 kb, discuss with your instructor.

---

## Repository Structure

```
htgaa-projects/
├── README.md
├── skills/
│   └── SKILL.md            ← skill definition (edit to update behaviour)
└── projects/               ← generated proposals saved here
    └── yourname_idea.md
```

---

## Troubleshooting

**`claude` command not found**
→ Make sure Claude Code is installed: `npm install -g @anthropic-ai/claude-code`
→ Make sure Node.js 18+ is installed: `node --version`

**Login / authentication errors**
→ Run `claude` and follow the browser prompt to log in with your Claude.ai account
→ Google sign-in is supported if your Claude.ai account uses Google
→ Confirm you have an active Claude Pro or Max subscription

**Skill not found / `/htgaa-final-project` not recognised**
→ Confirm you launched `claude` from inside the `htgaa-projects/` directory
→ Confirm `skills/SKILL.md` exists and the frontmatter `name:` field is `htgaa-final-project`

**Proposal not appearing in `projects/`**
→ The folder is created automatically — check that Claude Code has write permission to the directory
→ You can also ask the AI directly: "where did you save the proposal?"
