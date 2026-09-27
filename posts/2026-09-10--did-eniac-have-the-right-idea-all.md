---
title: "Did ENIAC Have the Right Idea All Along?"
subtitle: "ENIAC’s plugboards lost to EDVAC’s stored programs, but are resurgent in the age of AI"
date: 2026-09-10
slug: did-eniac-have-the-right-idea-all
canonical_url: "https://www.avikde.me/p/did-eniac-have-the-right-idea-all"
topic: "Uncategorized"
concepts:
  []
source: Substack
author: Avik De
---

# Did ENIAC Have the Right Idea All Along?

![](https://substackcdn.com/image/fetch/$s_!L8EV!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F25d23b44-07c5-4fa9-a5e9-5cf2c9a895f8_1595x523.png)

*ENIAC’s plugboards lost to EDVAC’s stored programs, but are resurgent in the age of AI*

> Originally published: [2026-09-10](https://www.avikde.me/p/did-eniac-have-the-right-idea-all)

**Citations:** [[citations/upenn-edu|upenn.edu]] · [[citations/mit-edu|mit.edu]] · [[citations/ieee-org|ieee.org]] · [[citations/columbia-edu|columbia.edu]] · [[citations/archive-org|archive.org]] · [[citations/en-wikipedia-org|en.wikipedia.org]] · [[citations/nextplatform-com|nextplatform.com]] · [[citations/chipinsights-net|chipinsights.net]]

---

At the Moore School of Electrical Engineering at the University of Pennsylvania, where I am now Adjunct Faculty, they have been celebrating the [80-year anniversary of ENIAC](<https://penntoday.upenn.edu/news/penns-eniac-worlds-first-electronic-computer-turns-80>). The Moore School is considered the birthplace of the computer industry, and ENIAC is regarded as the world’s first programmable, Turing-complete, electronic computer. The [New History of Modern Computing](<https://mitpress.mit.edu/9780262542906/a-new-history-of-modern-computing/>) also argues that ENIAC, more than Babbage’s difference engine, or the work of Alan Turing, had the largest influence on today’s computing landscape.

But digging a bit deeper, the way ENIAC worked would be unrecognizable to a current student of computer engineering. In contrast, ENIAC’s much less known successor, EDVAC, would actually be remarkably familiar. ENIAC and EDVAC represent two very different ideas of what “programming” is, with implications that are becoming extremely relevant in today’s AI age.

In this article, we’ll take a look at how ENIAC and EDVAC were programmed, why in some ways it is more appropriate to think of EDVAC as being the ancestor of modern computing than ENIAC, and how we might be about to do a U-turn back toward the ENIAC paradigm today.

Thanks for reading! Subscribe for free to receive new posts and support my work.

_This post is co-written with , who writes __. If you like this kind of post, make sure to subscribe for new ones!_

##  ENIAC’s programmers

Other than the computer itself, ENIAC also gave us the first known “programmers,” whose [story was widely popularized](<https://spectrum.ieee.org/the-women-behind-eniac>) only in the last 10 years. Quoting the [Penn Today article](<https://penntoday.upenn.edu/news/penns-eniac-worlds-first-electronic-computer-turns-80>):

> Programming this flexibility required what historians have described as a “physical hack” of the hardware, and the[ work fell to six pioneering women](<https://penntoday.upenn.edu/news/worlds-first-general-purpose-computer-turns-75>): Frances Bilas Spence, Jean Jennings Bartik, Ruth Lichterman Teitelbaum, Betty Snyder Holberton, Kay McNulty Mauchly Antonelli, and Marlyn Wescoff Meltzer. As the first digital-age programmers, they translated logic into electronic signals for ENIAC to interpret.

But what exactly did the programmers’ work (this “physical hacking”) look like?

ENIAC’s logic was distributed across 40 individual modular panels that acted as distinct arithmetic, control, and memory units. To solve a particular problem, the programmers drafted and followed “configuration diagrams” to reconfigure the wires and switches when changing between problems.

Columbia University’s Computing History archive has [an example of one of these configuration diagrams](<https://www.columbia.edu/cu/computinghistory/eniac.html>):

[![](https://substackcdn.com/image/fetch/$s_!L8EV!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F25d23b44-07c5-4fa9-a5e9-5cf2c9a895f8_1595x523.png)](<https://substackcdn.com/image/fetch/$s_!L8EV!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F25d23b44-07c5-4fa9-a5e9-5cf2c9a895f8_1595x523.png>)

The programmers’ task was not easy, as suggested by the diagram and this passage:

> One of the peculiarities that distinguished ENIAC from all later computers was the way in which instructions were set up on the machine. It was similar to the plugboards of small punched-card machines, but here we had about 40 plugboards, each several feet in size. A number of wires had to be plugged for each single instruction of a problem, thousands of them each time a problem was to begin a run; and this took several days to do and many more days to check out. When that was finally accomplished, we would run the problem as long as possible, i.e. as long as we had input data, before changing over to another problem. Typically, changeovers occurred only once every few weeks.

Because of the expertise the programmers developed, they helped scientists and engineers formulate their problems as sequences of ENIAC operations and converted the sequences to diagrams.

This process, going from wiring diagrams → problem decomposition → physical rewiring, is ENIAC’s version of “programming.”

A modern C compiler would be no help in programming ENIAC!

[Subscribe now](<https://www.avikde.me/subscribe?>)

In this paradigm, it would have made intuitive sense to minimize wiring, because it saves wire and reduces the possibility of misconfiguration. We’ll come back to this.

## EDVAC’s lasting legacy

Even in the early years of ENIAC, its creators Eckert and Mauchly were working on a draft for a new machine called EDVAC. At the same, [a certain John von Neumann](<https://www.avikde.me/p/what-von-neumann-understood-about>) took an interest in and joined this project. The written result of this collaboration, the _[First Draft of a Report on the EDVAC](<https://archive.org/details/firstdraftofrepo00vonn>)_ (1945) is, without exaggeration, a blueprint for modern computer organization and architecture. It was publicly circulated by Herman Goldstine before it could be patented by Eckert and Mauchly, and therefore slipped into public domain, to the benefit of the field of computer engineering as we know it today. In fact, this is the reason we call it the “von Neumann architecture” (the name on the _First Draft_) rather than the “Eckert-Mauchly architecture.”

The _First Draft_ articulated three key concepts that underpinned several EDVAC-like machines.

The first was the existence of a large high-speed memory which enabled this paradigm. Fortunately for the EDVAC project, [Williams tubes](<https://en.wikipedia.org/wiki/Williams_tube>) first demonstrated working random-access memory in 1946. ENIAC had no addressable memory at all — data just resided in the accumulators or function tables and had to be precisely clocked between them.

The second and most important was the “stored-program concept,” where instructions and data are stored in the same memory. “Programming” meant loading instructions onto this memory.

The third concept is to do with instruction codes (read from instruction memory) that could be used to direct the control circuitry on how to process data.

[![](https://substackcdn.com/image/fetch/$s_!w5FN!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F62e45222-1c68-4b81-b4c8-c2a3cc5715c6_960x556.png)](<https://substackcdn.com/image/fetch/$s_!w5FN!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F62e45222-1c68-4b81-b4c8-c2a3cc5715c6_960x556.png>)

The _First Draft_ ’s lasting legacy is that this architecture has been followed by CPUs from EDVAC all the way to now, and will be for the foreseeable future.

A modern C compiler could likely be made to generate an instruction sequence that could run on EDVAC!

[Subscribe now](<https://www.avikde.me/subscribe?>)

## A resurgence of ENIAC’s concept?

The physically demanding and highly specialized task of reconfiguring plugboards, as well as the increasing availability of memory, played a part in ushering in the stored-program era. It helped us create tools like high-level languages, compilers, and made programming accessible to a very broad audience.

However, it did have a cost.

ENIAC’s primary assignment was to speed up ballistic computations, not to be flexible. In a general purpose stored-program computer like EDVAC, the _physical movement of data_ was abstracted away so that the same hardware could run different tasks. As a tradeoff for this programmability, executing a single instruction could take hundreds of fetches of data from registers, caches, or main memory.

ENIAC’s wiring diagrams, in contrast, bring the flow of data to the forefront. Defining a computation meant literally plugging in wires on a plugboard. Data could (and likely would) be made to take the most efficient path to reach the accumulators, multipliers and function tables used to perform the arithmetic operations

Fast forward to today, and with “[Computing’s energy problem](<https://ieeexplore.ieee.org/document/6757323>),” the inefficient movement of data is driving a lot of innovation in computer architecture. Even the picojoules required to move data to the adders and multipliers, when done trillions of times, slows down computations and can consume a lot of energy!

Taalas, the Toronto-based startup now being acquired by AMD, accelerates deep neural networks by etching model weights into the ROM of the chip and paying very close attention to each transistor and connection for the least expensive multiply-accumulate operations possible:

> _We actually designed all this stuff from scratch internally. We didn’t use off the shelf anything, we did lots of transistor level design, hand layout – basically our whole effort ended up being a throwback to the 1970s._

In [this article](<https://www.nextplatform.com/compute/2026/02/19/taalas-etches-ai-models-onto-transistors-to-rocket-boost-inference/4092140>), their VP of products, Paresh Kharya, specifically calls back to ENIAC while talking about Taalas’s technology.

A less exotic direction several other efforts are pointing toward is a [dataflow architecture](<https://en.wikipedia.org/wiki/Dataflow_architecture>). I’ve previously mentioned the SambaNova RDU where data moves directly between functional units instead of through a central memory bottleneck:

[![](https://substackcdn.com/image/fetch/$s_!y6gs!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffcb9d42b-bf1a-4bd5-bb0e-586effbf01d7_2048x1152.png)](<https://substackcdn.com/image/fetch/$s_!y6gs!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffcb9d42b-bf1a-4bd5-bb0e-586effbf01d7_2048x1152.png>)

Physically connecting the plugboards seems like a nice proxy reminder of the fact that the cost of memory movement can’t be ignored. With the most innovative breakthroughs of today, it seems like we are going back in time!

In dataflow architectures, the compiler needs to do a lot more to lay out the computation physically on to the chip. But when the task is predictable and energetic efficiency is paramount, that could easily be a worthwhile tradeoff. It just needs expert “programmers” — like ENIAC had.

_Thanks for reading! If you enjoyed this post, please like (❤️) and restack — it helps others find my writing. Subscribe to receive new posts._

[ Share](<https://www.avikde.me/p/did-eniac-have-the-right-idea-all?utm_source=substack&utm_medium=email&utm_content=share&action=share>)

[Subscribe now](<https://www.avikde.me/subscribe?>)

## Further Reading

  * Thomas Haigh & Paul Ceruzzi, _[A New History of Modern Computing](<https://mitpress.mit.edu/9780262542906/a-new-history-of-modern-computing/>)_ (MIT Press, 2021)

  * John von Neumann, _[First Draft of a Report on the EDVAC](<https://archive.org/details/firstdraftofrepo00vonn>)_ (1945)

  * In this post, we didn’t go into the rich story of ENIAC’s development, for which I’ll point you to some great writing on substack:




[![](https://substackcdn.com/image/fetch/$s_!Z-fT!,w_56,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F74222e4c-9d04-46aa-82ba-7d82759b48b9_512x512.png)Chip InsightsENIAC and the Workload ProblemRead more7 months ago · 12 likes · 4 comments · Bharath Suresh](<https://chipinsights.net/p/eniac-and-the-workload-problem-part?utm_source=substack&utm_campaign=post_embed&utm_medium=web&embedding_publication_id=7287367>)

[![](https://substackcdn.com/image/fetch/$s_!vwjY!,w_56,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fffe682d7-ab93-463b-b714-8f98c0c072d2_1280x1280.png)The Chip LetterHerman Goldstine and the IAS Machine: Unveiling the Modern ComputerSometimes even men from the future need a little help…Read more3 years ago · 13 likes · 1 comment · Babbage](<https://thechipletter.substack.com/p/unveiling-the-modern-computer?utm_source=substack&utm_campaign=post_embed&utm_medium=web&embedding_publication_id=7287367>)
