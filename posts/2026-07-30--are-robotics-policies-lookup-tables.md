---
title: "Are Robotics Policies Lookup Tables?"
subtitle: "Practically yes, but there might be a solution"
date: 2026-07-30
slug: are-robotics-policies-lookup-tables
canonical_url: "https://www.avikde.me/p/are-robotics-policies-lookup-tables"
topic: "Uncategorized"
concepts:
  []
source: Substack
author: Avik De
---

# Are Robotics Policies Lookup Tables?

![](https://substackcdn.com/image/fetch/$s_!9y_3!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3636cf7d-d06f-4fbc-8ff6-c49a405cc4f4_500x333.jpeg)

*Practically yes, but there might be a solution*

> Originally published: [2026-07-30](https://www.avikde.me/p/are-robotics-policies-lookup-tables)

**Citations:** [[citations/whattotelltherobot-com|whattotelltherobot.com]] · [[citations/en-wikipedia-org|en.wikipedia.org]] · [[citations/neelnanda-io|neelnanda.io]] · [[citations/arxiv-org|arxiv.org]] · [[citations/mit-edu|mit.edu]] · [[citations/github-io|github.io]] · [[citations/pi-website|pi.website]]

---

Generalist robotics policies (such as Vision-Language-Action or [VLA](<https://www.avikde.me/p/debugging-as-architecture-insight>) models) have made frequent appearances on this blog. These huge models have performance and generalization characteristics that surpass our theoretical understanding, which is great for robot demonstrations, but not as good for deployment in safety-critical work.

While I was pondering how to discuss this for robotics policies in particular, researcher David Watkins and Professor Stefanie Tellex published an article on viewing a diffusion policy as a lookup table. The article is refreshing because it undoes some of the complexity of the black box; I’d definitely recommend adding it to your reading list:

[![](https://substackcdn.com/image/fetch/$s_!0Mfu!,w_56,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffee6e279-53b0-4949-804e-4f7aa106f40a_727x727.png)What to Tell the RobotDiffusion Policies are Fancy Lookup TablesHow do you know what data to collect so your robot learns the policy you want? Most answers hide inside talk about what the model "knows" or "understands," language we borrowed from describing people. Ben Burchfield once said a diffusion policy has the memory of a goldfish, since it stays Markov in the state it sees right now. Give up the mentalistic vo…Read more18 days ago · 8 likes · 1 comment · David Watkins and Stefanie Tellex](<https://whattotelltherobot.com/p/diffusion-policies-are-fancy-lookup?utm_source=substack&utm_campaign=post_embed&utm_medium=web&embedding_publication_id=7287367>)

Is that an architectural limitation, or a practical one? While the interpolation view of deep neural networks is a good starting point, we have quite a bit of evidence from different applications that they empirically exceed that characterization. In this post, I wanted to look at some alternate views of deep neural networks that promise greater computational capability and generalization than a lookup table, and see if they apply to robot actions policies.

Thanks for reading min{power}! Subscribe for free to receive new posts and support my work.

## The “grokking” phenomenon

An interpolator or lookup table intuitively can do no better than hit every single training data point. When it does that, the “training loss” goes down to 0, and there is nothing more to do… right? Surprisingly, it has been found that continuing to train after that point somehow results in continued improvement in _test time loss_ that can’t really be explained by interpolation of training data. This phenomenon has been called [grokking](<https://en.wikipedia.org/wiki/Grokking_\(machine_learning\)>):

[![](https://substackcdn.com/image/fetch/$s_!nkH4!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fad313ae9-666a-456c-b2f8-842467a8b407_1280x720.jpeg)](<https://substackcdn.com/image/fetch/$s_!nkH4!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fad313ae9-666a-456c-b2f8-842467a8b407_1280x720.jpeg>)By Neel Nanda - [Source](<https://www.neelnanda.io/mechanistic-interpretability>)

In 2023, [Gromov showed](<https://arxiv.org/abs/2301.02679>) that this can occur even with very small feedforward MLPs:

[![](https://substackcdn.com/image/fetch/$s_!znTs!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F71f8c1f8-a240-48a9-9392-f5ff6aea59f9_813x585.png)](<https://substackcdn.com/image/fetch/$s_!znTs!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F71f8c1f8-a240-48a9-9392-f5ff6aea59f9_813x585.png>)

Could robotics policies exhibit grokking and generalize actions outside their training datasets?

I think the answer to this is no, and I’ll give some reasons for this:

  1. The cases where grokking has been observed are supervised classification-style tasks with very clear objectives, with the test set and training set having very similar characteristics (they are drawn from the same distribution). This is a much more difficult claim to make for robot actions; even the objective is difficult to state.

  2. The modular arithmetic task has an algebraic symmetry structure that can be literally encoded in a neural network (i.e. you could hand-design a network that exactly solves the task). Robotics tasks are much more messy — maybe there is a [low-dimensional structure that encodes the solution](<https://www.avikde.me/p/the-ai-world-models-debate-and-its>), but it’s not really obvious that that exists.




In summary, while deep neural networks have demonstrated unexpected generalization capability, this is practically unlikely with robotics action-generation policies. In that situation, the “fancy lookup table” view is appropriate, with the ensuing failure modes described in the Watkins & Tellex post.

## The dynamical systems view

A second factor to consider is that robots continually interact with the environment, causing the policy to become a component in a dynamical system. Even smooth, simple dynamical systems can produce very complex and even chaotic behavior:

[![](https://substackcdn.com/image/fetch/$s_!6U_Y!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc47ff929-5103-4d09-9d78-d86a68a6a32d_1233x802.png)](<https://substackcdn.com/image/fetch/$s_!6U_Y!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc47ff929-5103-4d09-9d78-d86a68a6a32d_1233x802.png>)The stable equilibria of a simple dynamical system used to model population dynamics (the logistic map). [Source](<https://en.wikipedia.org/wiki/Bifurcation_diagram>)

LLMs which generate their tokens autoregressively (iteratively, one after the other) are also dynamical systems! There is evidence (from a [Merrill et. al ICLR 2024 paper](<https://arxiv.org/abs/2310.07923>)) that iterative reasoning genuinely moves an LLM up to a computational class that can solve any polynomial-time algorithm.

[![](https://substackcdn.com/image/fetch/$s_!1pu4!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F383413c7-0b87-4bda-a1aa-09c357178ee1_808x511.png)](<https://substackcdn.com/image/fetch/$s_!1pu4!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F383413c7-0b87-4bda-a1aa-09c357178ee1_808x511.png>)

They show that this effect is specifically because of the autoregressive text generation, i.e. the dynamical system effect, and not the underlying transformer architecture.

* * *

Returning to robotics, in my previous article on embodied intelligence, I talked about Rodney Brooks’ subsumption architecture and its view of the “world being the model” — it doesn’t make sense to even talk about the policy without looking at its interaction with the world.

A robotics policy is always situated in a dynamical system:
    
    
    observation1 = Sensing(state1) # Robot sensing
    action1 = Policy(observation1) # Robot policy
    state2 = World(state1, action1) # The dynamics of the world
    # ... and repeat

Does this effect help upgrade a robotics policy from a lookup table?

I believe the answer to this is no, and I have an intuitive explanation for why.

In an autoregressive LLM loop, it generates the “scratchpad” itself, and it can address it by the attention mechanism. These two aspects form a remarkable connection to a [Turing machine](<https://en.wikipedia.org/wiki/Turing_machine>)!

> A **Turing machine** is a mathematical model of computation describing an abstract machine that manipulates symbols on a strip of tape according to a table of rules. Despite the model’s simplicity, it is capable of implementing any computer algorithm.

[![A physical Turing machine constructed by Mike Davey](https://substackcdn.com/image/fetch/$s_!9y_3!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3636cf7d-d06f-4fbc-8ff6-c49a405cc4f4_500x333.jpeg)](<https://substackcdn.com/image/fetch/$s_!9y_3!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3636cf7d-d06f-4fbc-8ff6-c49a405cc4f4_500x333.jpeg>)

Replace “strip of tape” with “scratchpad,” the “manipulation of symbols” with the generation of reasoning tokens and lookup using self-attention, and it appeals strongly to intuition _why_ Merrill et al found the computational class upgrade.

[Subscribe now](<https://www.avikde.me/subscribe?>)

In contrast, the typical memoryless robot policy doesn’t really get to store arbitrary items on the tape, nor look them up at will. While the policy interacts with the world, there is no guarantee that the observation [contains all the ncessary information](<https://en.wikipedia.org/wiki/Markov_decision_process>), leading us to a partially-observable Markov decision process (POMDP). In fact, the classic [Kaelbling et al 1998 paper](<https://people.csail.mit.edu/lpk/papers/aij98-pomdp.pdf>) (with over 7000 citations!) shows that the optimal policy for a POMDP is a function of the entire belief state (given the entire observation-action history) and not of the instantaneous observation, and discusses how finite-memory controllers can be extracted in some cases.

* * *

There have been recent efforts to imbue robotics policies with the same “scratchpad” capabilities; for example see the Zawalski et al 2024 [Embodied Chain-of-Thought](<https://embodied-cot.github.io/>) paper, and the [pi0.7 model](<https://www.pi.website/blog/pi07>), which both generate subtasks before the action.

[![](https://substackcdn.com/image/fetch/$s_!9u7o!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc61349a1-fc1d-4fbf-9c5f-3085c24749ea_3325x889.png)](<https://substackcdn.com/image/fetch/$s_!9u7o!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc61349a1-fc1d-4fbf-9c5f-3085c24749ea_3325x889.png>)

However, these efforts are in the perception / cognition part of the pipeline; the action head itself is still lookup-table-class and has exactly the limitations that Watkins & Tellex describe in their post. I.e., while you can get generalization at the larger behavioral level, the actions themselves will be interpolations of those in training datasets.

## Actually moving beyond lookup tables

The behavior of even simple deep neural networks can be inexplicable by theory (e.g. the Gromov reference above), and even less is known formally about complex robotics policies. In this post, we went over a couple of ways that these policies could potentially sneak up to be more than interpolators of their training data. Still, in practical terms today, most action heads are lookup tables.

However, there are ways to move beyond that! At the [end of my embodied intelligence post](<https://www.avikde.me/i/199171451/a-potential-resolution>) I described the potential benefits of action generation using reinforcement learning (RL) or model-based control. These techniques have the ability to not only consider embodiment and environment features (the prior article’s point), but also generalize beyond any collected data.

RL generates its own data (though it is typically defined at the training stage) and model-based control will effectively explore and generate new solutions online. There are [some](<https://lucid-robot.github.io/>) approaches in the literature emerging to try and combine these strengths with a foundation model for perception and cognition, but it is far from a common paradigm, and I haven’t seen careful studies of the resulting generalization capabilities yet. It’s an area of research that I believe is quite promising and will be keeping an eye on!

_Thanks for reading! If you enjoyed this post, please like (❤️) and restack — it helps others find my writing. Subscribe to receive new posts._

[ Share](<https://www.avikde.me/p/are-robotics-policies-lookup-tables?utm_source=substack&utm_medium=email&utm_content=share&action=share>)

[Subscribe now](<https://www.avikde.me/subscribe?>)
