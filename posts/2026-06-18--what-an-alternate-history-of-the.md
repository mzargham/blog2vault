---
title: "What an Alternate History of the RISC vs. CISC Debate Teaches Us About Robotics"
subtitle: "Remove the compiler layer, and RISC's ecosystem advantages invert"
date: 2026-06-18
slug: what-an-alternate-history-of-the
canonical_url: "https://www.avikde.me/p/what-an-alternate-history-of-the"
topic: "Uncategorized"
concepts:
  []
source: Substack
author: Avik De
---

# What an Alternate History of the RISC vs. CISC Debate Teaches Us About Robotics

![](https://substackcdn.com/image/fetch/$s_!IAZS!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5c2857f9-887c-4e16-82d2-3b19b74eaef9_1536x1024.png)

*Remove the compiler layer, and RISC's ecosystem advantages invert*

> Originally published: [2026-06-18](https://www.avikde.me/p/what-an-alternate-history-of-the)

**Citations:** [[citations/chipinsights-net|chipinsights.net]] · [[citations/chipsandcheese-com|chipsandcheese.com]] · [[citations/famberzbuilt-in|famberzbuilt.in]] · [[citations/en-wikipedia-org|en.wikipedia.org]] · [[citations/arxiv-org|arxiv.org]] · [[citations/sifted-eu|sifted.eu]]

---

Recently, Elon Musk [staked a claim](<https://x.com/elonmusk/status/2021745508277268824>) that LLMs would eliminate the need for high-level computer programming languages, since they could compile directly to machine code.

[![](https://substackcdn.com/image/fetch/$s_!zdRc!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F726eb415-21bd-4b47-9dae-1423a50159ba_1044x392.png)](<https://substackcdn.com/image/fetch/$s_!zdRc!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F726eb415-21bd-4b47-9dae-1423a50159ba_1044x392.png>)

Effectively, underlying that claim is a comparison between two pathways:

[![](https://substackcdn.com/image/fetch/$s_!IAZS!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5c2857f9-887c-4e16-82d2-3b19b74eaef9_1536x1024.png)](<https://substackcdn.com/image/fetch/$s_!IAZS!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5c2857f9-887c-4e16-82d2-3b19b74eaef9_1536x1024.png>)

You’ll notice that the new pathway bypasses or short-circuits an important layer of abstraction in modern computing, the Instruction Set Architecture (ISA). Associated with that, it also eliminates the compiler. Importantly, it doesn’t eliminate instructions; ultimately, those need to be emitted either way in order to drive the hardware.

The question of what characteristics the ISA should have spawned the great [RISC vs. CISC debate](<https://chipinsights.net/p/the-isa-debate>) in computer engineering. We still use both RISC and CISC architectures, so it’s a subtle debate with merits on both sides. It also had some formative effects on the history of computer engineering, such as:

  * The nature of the hardware ecosystem — how much it favors incumbents vs. new entrants

  * The nature of hardware innovation — how viable different hardware architectures are

  * The process by which software is interfaced to and optimized for hardware — compilers, toolchains, etc.




The ISA debate itself is not the locus of innovation any longer, but it has had substantial influence on how desktop, mobile, and server computing have developed. That’s all history now.

However, what if AI’s capabilities had arrived 30 years sooner, and Musk’s proposed scheme was the accepted software development paradigm? Would the RISC vs. CISC debate look the same?

On a separate note, in my [previous post](<https://www.avikde.me/p/action-tokens-fine-grained-vs-behavioral>) I discussed the importance of action tokens in robotics. Their granularity is an important design choice for robotic systems, and we have seen them range from very fine (joint commands) to very coarse (behavioral primitives). These are analogous to RISC and CISC instructions! However, importantly, robotics [does not have the notion of an ISA or a compiler](<https://www.avikde.me/p/a-multi-robot-brain-is-not-like-a>). The results of this alternate history of computing may be quite relevant to answering some of the big questions about how a “robotics ecosystem” shapes up over the coming years.

In the following sections, we’ll go over:

  * A very brief review of the key points in RISC vs. CISC debate, and how they have shaped computing’s landscape

  * What the landscape may have looked like without the ISA layer

  * What this means for robotics




 _If you enjoy this post, please consider sharing and subscribing for free. I recently had one of my posts get[published in IEEE Spectrum magazine](<https://substack.com/@avikde/note/c-277881308?r=5vzx85&utm_source=notes-share-action&utm_medium=web>), and I’m incredibly grateful for the reader support that helped make that possible._

[Share](<https://www.avikde.me/p/what-an-alternate-history-of-the?utm_source=substack&utm_medium=email&utm_content=share&action=share>)

 _This article is co-written with. Subscribe to  for narrative and insightful posts on computer architecture._

[![](https://substackcdn.com/image/fetch/$s_!Z-fT!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F74222e4c-9d04-46aa-82ba-7d82759b48b9_512x512.png)Chip InsightsSemiconductor Industry Deep DivesBy Bharath Suresh](<https://chipinsights.net?utm_source=substack&utm_campaign=publication_embed&utm_medium=web>)

## The RISC vs. CISC Debate and its Implications

RISC instructions do very simple bits of work, which means many instructions are needed to solve a complex task. The compiler does the job of breaking up a complex task into these small steps. CISC instructions, on the other hand, can have the CPU do large bits of a task in a single dispatch. x86, a CISC architecture, has dominated desktop computing for several decades, while Arm, a RISC architecture, has dominated the mobile market. The RISC vs. CISC debate wouldn’t exist if there was a clear winner, which means that both sides have merits and tradeoffs. For curious readers, I’ve linked further resources below, but I wanted to highlight some of the broader ecosystem implications of one vs. the other:

The simplicity of the RISC instructions makes it easier to build hardware: the ISA is simpler to implement, and this leads to **relatively more hardware entrants**. This has been shown to be true in computing, with a [Cambrian explosion of RISC entrants](<https://thechipletter.substack.com/p/the-risc-wars-part-1-the-cambrian-c55>).1 Most computer organization and architecture courses build a RISC processor, and there are significantly more freely available resources that assist this process.

Because the RISC ecosystem is easier to enter, we tend to see **more diversity in the microarchitecture**. A good example is the [Condor Cuzco RISC-V core](<https://chipsandcheese.com/p/condors-cuzco-risc-v-core-at-hot>). Considering memory access time, different instructions require different amounts of latency in processors, and optimal performance requires scheduling instructions at precise times so that their operands are available. NVIDIA does this scheduling in their GPU compiler, but the RISC-V ISA leaves room for it to be implemented in hardware. Condor implements a “Time-Resource Matrix” solver for this problem, an innovative solution that they can pursue by **relying on existing RISC-V infrastructure to build on**.

The burden of **software optimization** is moved to the compiler by RISC. As  said in his article, RISC is an apt acronym of “Relegate Important Stuff To Compiler”. The saving grace is that this compiler complexity is shared over many hardware targets, enabled by the ISA. It would be impractical to expect LLVM to be able to produce optimized code for a processor I invent, whereas I can easily piggyback on existing work if I target an established ISA.

To summarize, RISC helps promote a more **open, thriving ecosystem, encourages innovation and diversity in hardware, and spreads out the burden of optimization** among different vertical parts of the stack (software, compiler, hardware).

## A Thought Experiment: no ISA or Compiler

Underlying both sides of the ISA debate, computer engineering has a foundation with two critical pieces of technology: the **ISA** itself, and the **compiler**.

Let’s imagine Musk’s proposed alternate world where these do not exist. To be clear, we are not advocating for this proposal (there is much [other writing](<https://engrlog.substack.com/p/why-skip-the-code-ship-the-binary>) on this topic) other than using it for a thought experiment. Programs would be converted directly into machine code from high-level intent by an LLM (though the specifics of the method aren’t important for the point). In this world, we could still have RISC and CISC processors; the LLM would just have to know and understand how to map to the different instruction sets. Essentially, the LLM becomes a general purpose compiler across multiple ISAs.

However, the ecosystem effects would not be the same, and in many ways would be inverted!

Underlying the vibrant RISC hardware ecosystem was the hidden assumption that the compiler abstracts over implementation differences. If we delegate that to an LLM, RISC’s simplicity _becomes a liability_. Every microarchitectural optimization or quirk is now the LLM’s responsibility to learn separately, and CISC’s philosophy of “let the hardware handle complexity” becomes an advantage.

It is still simpler to build RISC hardware, but without an ISA, the **complexity of the full stack** will fall entirely on the new hardware entrant. They cannot utilize work done by software or compiler authors, and will have to build or fine-tune a new LLM to target their hardware, with all the complexity that entails (datasets, benchmarks, training infrastructure, etc.). Practically, this makes it even more difficult than it already is for new hardware entrants.2

The LLM now needs to embed knowledge of all the microarchitectural variations in hardware. For economic viability, hardware entrants will be incentivized to maintain LLM compatibility in novel releases, **suppressing microarchitectural innovation**.

RISC vs. CISC also affects the **complexity of the LLM** that needs to be built to target the hardware. With CISC, fewer instructions are needed for the same program and the output space of the LLM is reduced. In fact, CISC was historically preferred for a similar reason: computer memory was slow and expensive.

In some cases, CISC can also help abstract hardware differences away. For example, the [REP MOVS](<https://thechipletter.substack.com/p/the-long-history-of-rep-movs>) x86 instruction is a full translation of the intent (“move a string”), while in a load-store RISC architecture that does not support memory-memory operations, the LLM needs to perform many steps, and to keep track of which registers are free to implement the equivalent.

Processors built on the CISC architectures have largely overcome their microarchitectural weaknesses by translating complex instructions into [micro-ops](<https://famberzbuilt.in/blog-details/micro-operations-ops-how-cpus-break-instructions-into-smaller-steps>) to achieve similar hardware efficiencies as their RISC counterparts. In the proposed alternate world, RISC would also lose out on the other advantage it currently holds: easier performance optimization by the compiler.

Putting this all together, we first realize that Musk’s proposal results in a significantly more consolidated ecosystem where **innovation in hardware is more difficult across the board, and architectural diversity is stifled**. A dark future indeed!

More unexpected is the realization that in this alternate future, **RISC hardware becomes disproportionately** _**more difficult**_**to build**. The ecosystem becomes more closed and concentrated, while CISC has a somewhat better chance of supporting different hardware with the same software.

## The Effects on Robotics

We’ve [written before about](<https://www.avikde.me/p/the-first-paradigm-in-robotics-and>) how computer engineering can anticipate aspects of technology development in the field of robotics. Could a RISC vs. CISC debate appear there, and have similar ecosystem effects?

Action tokens are analogous to instructions, and we have seen examples of [fine- or coarse-grained tokens in robotics](<https://www.avikde.me/p/action-tokens-fine-grained-vs-behavioral>). In a previous article I demonstrated that [both are viable for a tabletop manipulation task](<https://www.avikde.me/p/a-coding-agent-equivalent-for-robotics>).

A Vision-Language-Action (VLA) model is an example of a “RISC” software layer that outputs fine-grained actions, and the outputs can be **joint-level or Cartesian infinitesimal commands**. The “CISC” software layer requires effectively a high-level task orchestrator outputting **higher-level symbolic motion or task primitives** (like “grasp object”). We have seen examples of this in classical AI dating back to [STRIPS](<https://en.wikipedia.org/wiki/Stanford_Research_Institute_Problem_Solver>), as well as in modern AI with VLMs like Gemini ER.

Since an [ISA or compiler equivalent does not exist today](<https://www.avikde.me/p/a-multi-robot-brain-is-not-like-a>), we end up in the “alternate history” version of the world from the previous section. What can we learn from it about the future of robotics?

Building “RISC” robots with only joint-level control functions remains a simpler task than also endowing them with higher-level task functions and autonomy. However, for the robots to be useful, those software components still need to be obtained from somewhere. Without the ISA layer, this effectively means that the software layer needs to have native support for the new hardware.

For [my VLA project](<https://www.avikde.me/p/debugging-as-architecture-insight>), I made my simulated robot arm choice based on what was supported by a VLA out-of-the-box, and I assume this is a common phenomenon. The result is **consolidation and reduction of hardware diversity**.

A [2024 study](<https://arxiv.org/pdf/2512.12230>) on zero-shot fall recovery across seven humanoid morphologies found noted difficulty transferring to robots that are “top-heavy, long-armed, or otherwise distant in morphology space”. The CISC equivalent has been explored less, but this [2020 paper from Berkeley](<https://sites.google.com/berkeley.edu/morphology-transfer>) demonstrates that using “CISC” subgoals with a morphology dependent low-level policy aids policy transfer to new morphologies.

Lastly, with the RISC perspective, the burden of optimization is pushed entirely on to either the AI model builder, or the hardware vendor (who must now fine-tune the large model to work with their hardware). Unlike the multi-layer software → compiler → hardware stack, where smaller players can share the burden to build competent products, there is no way to spread this workload around. This affects ecosystem investment and control, both commercially and [in academic research](<https://www.avikde.me/p/the-first-paradigm-in-robotics-and>).

[Leave a comment](<https://www.avikde.me/p/what-an-alternate-history-of-the/comments>)

## Closing Thoughts

I have always had a fond impression of how RISC influenced the computing ecosystem, and it turns out that the ISA layer was a crucial reason for that. Elon Musk’s claim made me think of how that hypothetical scenario could have changed history, and it almost completely inverts the balance.

Robotics is early to this game, doesn’t have an equivalent of an ISA yet, and ecosystems are just beginning to take shape. For now, there are (very smart!) engineers at different research labs and companies choosing “instruction” granularity for their own technical reasons. As well they should — building a robotic solution poses enough challenges as it is. However, so were computer engineers at Intel, and it’s difficult to imagine the long-reaching ecosystem consequences of these decisions!

Even though robotics doesn’t have an “ISA” yet, there are some promising directions and paradigms I’d like to explore in an upcoming article. Make sure to subscribe for that, and thanks for reading!

_If you enjoyed this post, please like (❤️) and restack — it helps others find my writing. Subscribe to receive new posts. All of this is greatly appreciated._

[ Share](<https://www.avikde.me/p/what-an-alternate-history-of-the?utm_source=substack&utm_medium=email&utm_content=share&action=share>)

Thanks for reading min{power}! Subscribe for free to receive new posts and support my work.

## Further Reading

In this article I talked through an “action token” in robotics, an equivalent of an “instruction” in computing:

Read about the RISC-spurned ecosystem in computing:

[![](https://substackcdn.com/image/fetch/$s_!vwjY!,w_56,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fffe682d7-ab93-463b-b714-8f98c0c072d2_1280x1280.png)The Chip LetterThe RISC Wars Part 1 : The Cambrian ExplosionI’d like to start this week’s post with a small confession. In last week’s post, I called Berkeley RISC-I ‘the first RISC microprocessor’. In fact, some believe that a derivative of the IBM 801, known as ROMP, was the first RISC microprocessor. The story of the 801’s successors, including ROMP, will be the subject of a later post. I believe that RISC-I …Read more3 years ago · 29 likes · 24 comments · Babbage](<https://thechipletter.substack.com/p/the-risc-wars-part-1-the-cambrian-c55?utm_source=substack&utm_campaign=post_embed&utm_medium=web>)

1

There is an orthogonal topic of ISA _licensing_ which is unrelated to the RISC vs. CISC-ness, so we will skip over it for this article.

2

There have been real examples of cautionary tales of hardware startups deviating too far from existing ISAs / toolchains and suffering — Graphcore is probably the [cautionary tale](<https://sifted.eu/articles/graphcore-finances>). We are part way through an [article series](<https://chipinsights.net/p/mapping-algorithms-to-custom-silicon>) about how to approach this problem with the hands-on example of a matrix multiplication accelerator.
