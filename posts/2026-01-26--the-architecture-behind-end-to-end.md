---
title: "The architecture behind “end-to-end” robotics pipelines"
subtitle: "Part 1: Where the learning stack ends and the control stack begins"
date: 2026-01-26
slug: the-architecture-behind-end-to-end
canonical_url: "https://www.avikde.me/p/the-architecture-behind-end-to-end"
topic: "End-to-End Robotics Pipelines"
concepts:
  - "End-to-End Robotics Pipelines"
  - "Hardware Acceleration"
  - "Generalist Policies"
  - "Perception-Planning-Control Modules"
source: Substack
author: Avik De
---

# The architecture behind “end-to-end” robotics pipelines

![](https://substackcdn.com/image/fetch/$s_!766O!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc93dedb4-82d1-4d59-b085-1a7493ed6040_1200x900.jpeg)

*Part 1: Where the learning stack ends and the control stack begins*

> Originally published: [2026-01-26](https://www.avikde.me/p/the-architecture-behind-end-to-end)

**Topic:** [[topics/end-to-end-robotics-pipelines|End-to-End Robotics Pipelines]]
**Concepts:** [[concepts/end-to-end-robotics-pipelines|End-to-End Robotics Pipelines]] · [[concepts/hardware-acceleration|Hardware Acceleration]] · [[concepts/generalist-policies|Generalist Policies]] · [[concepts/perception-planning-control-modules|Perception-Planning-Control Modules]]
**Citations:** [[citations/en-wikipedia-org|en.wikipedia.org]] · [[citations/ieee-org|ieee.org]] · [[citations/mit-edu|mit.edu]] · [[citations/arxiv-org|arxiv.org]] · [[citations/figure-ai|figure.ai]] · [[citations/pi-website|pi.website]] · [[citations/bostondynamics-com|bostondynamics.com]] · [[citations/1x-tech|1x.tech]] · [[citations/courses-lumenlearning-com|courses.lumenlearning.com]] · [[citations/rodneybrooks-com|rodneybrooks.com]] · [[citations/github-io|github.io]]

---

_This article is part of a series on end-to-end robotics pipelines:_

  1. This article

  2. [Online motor adaptation](<https://www.avikde.me/p/is-it-learning-online-motor-adaptation?r=5vzx85>)

  3. [Dissecting a VLA](<https://www.avikde.me/p/debugging-as-architecture-insight>)

  4. [Closing the action loop with a VLM “agent”](<https://www.avikde.me/p/a-coding-agent-equivalent-for-robotics?r=5vzx85&utm_campaign=post&utm_medium=web>)

  5. [Demo combining the best features of end-to-end and classical approaches](<https://www.avikde.me/p/building-a-reasoning-hierarchical>)




* * *

Recent progress and excitement in humanoid robotics are largely driven by rapid gains in generalist capabilities. Historically, most robots were engineered for narrow, well-defined tasks. The current wave of companies, in contrast, is pursuing systems intended to operate across a broad range of activities, shifting both public and economic expectations toward robots that can serve as general-purpose physical agents.

A central part of this shift is the widespread claim of _end-to-end_ pipelines, often described as going from “pixels to actions,” in contrast to earlier approaches built from hand-designed perception, planning, and control modules. This post examines what “end-to-end” means in practice: where the pipeline actually begins and ends, the tradeoffs between different architectural choices, and how the algorithms map to computing hardware.

Part 1 focuses on the “actions” side of “pixels to actions”: how learned systems interface with the physical control of the robot body. Part 2 will examine how these architectures adapt to environmental uncertainty and contact-rich interaction. Later parts will include hands-on comparisons using small standalone examples to make these differences concrete.

Thanks for reading min{power}! Subscribe for free to receive new posts and support my work.

_This publication and this post contain the author’s personal thoughts and opinions only, and do not reflect the views of any companies or institutions._

### Why “end-to-end”

Classical AI was built up from a strict idea of separation of sensing, planning, and action. To my knowledge, the first robot to embody Sense-Plan-Act was [Shakey the robot](<https://en.wikipedia.org/wiki/Shakey_the_robot>) (~1970), which also employed one of the first [symbolic AI systems](<https://en.wikipedia.org/wiki/Stanford_Research_Institute_Problem_Solver>). This tiered structure was so formative to robotics research that most research labs today are dedicated to different portions of this hierarchy, such as “perception”, “planning”, or “locomotion”.

[![SRI researchers Nils Nilsson \(right\) and Sven Wahlstrom with Shakey the Robot in the late 1960s.](https://substackcdn.com/image/fetch/$s_!766O!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc93dedb4-82d1-4d59-b085-1a7493ed6040_1200x900.jpeg)](<https://substackcdn.com/image/fetch/$s_!766O!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc93dedb4-82d1-4d59-b085-1a7493ed6040_1200x900.jpeg>)Shakey the robot in the late 1960’s (photo from [here](<https://spectrum.ieee.org/sri-shakey-robot-honored-as-ieee-milestone>)).

The sense-plan-act view today is dying a very rapid death. The modern narrative of general-purpose robotics holds that modular pipelines often fail because of limitations imposed by this decoupling; for example, perception errors break planners, planners produce infeasible motions, and most importantly, interfaces encode wrong assumptions.

As influencial AI researcher [Sergey Levine puts it](<https://sergeylevine.substack.com/p/sporks-of-agi>),

> for any learning-enabled system, any component that is _not_ learned but instead designed by hand will eventually become the bottleneck to its performance

End-to-end training avoids hand-designed intermediate representations, manually tuned cost functions, and any bottlenecks imposed by module interfaces.

Additionally, “end-to-end” sends a sociological signal to do with modern AI foundation-model alignment, scalability with data, and positions the company as an AI lab instead of a controls shop.

### The action end in practice

The practical reality of “end-to-end” is more subtle than it might seem. In this section we’ll review what some published academic and commercial implementations actually appear to be doing today, and also try to outline how the implementation is mapped to computational hardware.

#### The old way: model-based stacks (~2014)

It is very common to have a whole-body controller at the low-level, as exemplified by the [2014 MIT Atlas team’s report](<https://groups.csail.mit.edu/robotics-center/public_papers/Kuindersma14.pdf>). After a high-level plan is created, a tracking controller is implemented as a quadratic program, and that generates the signals sent to the actuators:

[![](https://substackcdn.com/image/fetch/$s_!NdCg!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7ea62b32-540b-4439-9103-3401ae70d839_580x571.png)](<https://substackcdn.com/image/fetch/$s_!NdCg!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7ea62b32-540b-4439-9103-3401ae70d839_580x571.png>)Figure 6 from the [2014 MIT Atlas team’s report](<https://groups.csail.mit.edu/robotics-center/public_papers/Kuindersma14.pdf>) showing the low-level action pipeline, referred to as “Control.”

Mapping to computational hardware:

_Trajectory optimizer (CPU) → WBC inverse dynamics/QP (CPU) → Joint/servo controllers (microcontroller/CPU) → Torques_

#### Learning followed by impedance controller (~2017-2020)

To my knowledge, the first fielded robots using learning-based locomotion controllers appeared ~2018 from Google (using [Minitaur](<https://www.avikde.me/p/ghost-robotics-minitaur>)) and in Marco Hutter’s group. As documented in the [2018 paper from Google](<https://arxiv.org/pdf/1804.10332>) and the [highly-cited Hwangbo et al (2019) paper](<https://arxiv.org/pdf/1901.08652>), the most effective choice of action space was an impedance controller in turn influenced by [Peng et al (2017)](<https://arxiv.org/pdf/1611.01055>):

> Our experiments suggest that action parameterizations that include basic local feedback, such as PD target angles, MTU activations, or target velocities, can improve policy performance and learning speed across different motions and character morphologies

The policy outputs desired joint positions and sometimes velocity offsets or gain modulation, and the torque applied is a simple algebraic equation:

The virtue of this architecture is that it is very generic, and succeeds in decoupling the fast time-scales and discontinuities of making and breaking contact from the learning algorithm.

Mapping to computational hardware:

_Policy eval (CPU/embedded GPU) → Impedance controller (CPU) → Actuators_

#### Figure AI’s “System 1” policy (2025)

[Figure AI’s Feb 2025 blog post](<https://www.figure.ai/news/helix>) describes a “System 2 / System 1” design where a high-level vision-language model (S2) reasons about goals and semantics at low frequency, and a fast visuomotor network (S1) executes continuous control at high frequency. While this reflects a separation of timescales and roles, both modules are trained end-to-end with an abstract latent interface, meaning there is not a principled, physically interpretable handoff between high-level strategy and low-level control. As a result, Helix achieves generalization in perception and task reasoning but does not isolate physical control concerns (such as dynamics stabilization, contact interaction, or actuation abstraction) into structured model-based or classical control modules.

[![](https://substackcdn.com/image/fetch/$s_!Qh5X!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Feca99354-c9d3-466f-a3a5-d7a765c02d49_1322x596.png)](<https://substackcdn.com/image/fetch/$s_!Qh5X!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Feca99354-c9d3-466f-a3a5-d7a765c02d49_1322x596.png>)Figure AI’s architecture from [their blog post](<https://www.figure.ai/news/helix>).

In a [Mar 2025 blog post](<https://www.figure.ai/news/reinforcement-learning-walking>), they describe what sounds more like the impedance controller above than the system 1 design, so it’s possible some combination of both architectures is utilized:

> We additionally run the policy output through kHz-rate closed-loop torque control to compensate for errors in actuator modeling

Mapping to computational hardware:

_System 2 (Transformer, GPU) → System 1 (Network, GPU) → [Impedance control (CPU)] → Torques_

#### Physical Intelligence’s action expert (2025)

The [architecture described](<https://www.pi.website/research/knowledge_insulation>) is similar to the system 1 above, but specifically suggests that the end-to-end training causes problems:

> When adapting a VLM to a VLA in this action expert design, the VLM backbone representations are exposed to the gradients from the action expert. Our experiments show that those gradients from the action expert lead to unfavorable learning dynamics, which not only results in much slower learning, but also causes the VLM backbone to lose some of the knowledge acquired during web-scale pre-training.

This is conceptually analogous to known problems like [vanishing/exploding gradients](<https://en.wikipedia.org/wiki/Vanishing_gradient_problem>) in deep nets, where lower layers dominate or drown out meaningful gradients for higher layers.

[![](https://substackcdn.com/image/fetch/$s_!Ll11!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2a921377-0f3c-4390-ae1d-9b4de26babd8_1295x595.png)](<https://substackcdn.com/image/fetch/$s_!Ll11!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2a921377-0f3c-4390-ae1d-9b4de26babd8_1295x595.png>)Physical Intelligence’s architecture from [their blog post](<https://www.pi.website/research/knowledge_insulation>).

Another blog post describes issues to do with the mismatched control bandwidth of foundation model output to robot dynamics, solved by [outputting short horizon trajectories](<https://www.pi.website/research/real_time_chunking>) that are played out by a low-level controller.

Mapping to computation:

_VLM (GPU) → Action expert (GPU/CPU) → Trajectory tracking (CPU) → Torques_

#### Boston Dynamics + TRI’s pose tracking (2025)

Their [blog post describes](<https://bostondynamics.com/blog/large-behavior-models-atlas-find-new-footing/>) an architecture with the higher-level cognitive layer outputs joint positions and end-effector poses. While there isn’t an explicit decription of how these position setpoints are tracked, the post mentions Atlas’s MPC, and it is reasonable to assume that that is the lower-level controller.

[![Our policy maps inputs consisting of images, proprioception and language prompts to actions that control the full Atlas robot at 30Hz. We leverage a diffusion transformer together with a flow matching loss to train our model.](https://substackcdn.com/image/fetch/$s_!JBTF!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe2410984-5712-4c1b-bdcb-55e45fe63d1f_1024x372.png)](<https://substackcdn.com/image/fetch/$s_!JBTF!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe2410984-5712-4c1b-bdcb-55e45fe63d1f_1024x372.png>)Boston Dynamics + TRI architecture from [their blog post](<https://bostondynamics.com/blog/large-behavior-models-atlas-find-new-footing/>).

Mapping to computational hardware:

_LBM inference (GPU) → MPC (CPU) → Actuator torques_

#### 1X’s inverse dynamics model IDM (2026)

1X also describes a hierarchy in [their blog post](<https://www.1x.tech/discover/world-model-self-learning>):

[![](https://substackcdn.com/image/fetch/$s_!F2IG!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4953307e-d6f5-4b45-b35c-f5c13ccf29f4_1041x628.png)](<https://substackcdn.com/image/fetch/$s_!F2IG!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4953307e-d6f5-4b45-b35c-f5c13ccf29f4_1041x628.png>)1X architecture from [their blog post](<https://www.1x.tech/discover/world-model-self-learning>).

World Model Backbone (WM): A text-conditioned video prediction model trained on internet-scale video data and fine-tuned on robot sensorimotor data. It predicts future visual states based on current observations and candidate actions.

Inverse Dynamics Model (IDM): Converts predicted future states into feasible robot action sequences that will produce those outcomes in the real world. The use of the term “inverse dynamics” suggests that the output actions are torques, though that isn’t specified.

Mapping to computational hardware:

_World model (GPU) → IDM (GPU) → Actuator torques_

### Why not end-to-end

From the previous section, it is apparent that “end-to-end” doesn’t usually mean that a single algorithm or network is going from pixels to torques. In this section, we’ll try to list some potential intuitive reasons for this.

#### Separation of concerns

We saw above on Physical Intelligence’s blog post that there are difficulties in training an end-to-end policy that does so many different things. [Another quote](<https://www.pi.website/research/knowledge_insulation>):

> One hypothesis of why this is happening is the following. A pre-trained VLM, by its nature, pays attention to language inputs well. The gradients from the action expert now severly interfere with the model’s ability to process language, which leads the model to pick up on other correlations first.

These problems are a side-effect of one network trying to solve a lot of different problems. The old Sense-Plan-Act schema enforced a separation of concerns very strictly, but even with a more relaxed architecture, low-level control priors drastically reduce the policy search space.

A human nervous exhibits similar separation with a cortex (goal-directed commands), cerebellum (fast adaptation, prediction), spinal reflexes (fast control loops), and even mechanical impedance control in muscles / tendons.

[![This diagram shows the complete pathway a nerve impulse takes when a person tests the temperature of shower water with their hand. First, a sensory nerve ending in the index finger sends a nerve impulse to the spinal cord. A cross section of one segment of the vertebrae is shown from a superior view. The sensory nerve connected to the nerve ending is located in the dorsal root ganglion. The nerve ending is a dendrite of the sensory neuron, as it also has an axon that synapses with an interneuron. The interneuron then synapses with a second interneuron in the thalamus. This second interneuron synapses with brain tissue in the cerebral cortex, allowing conscious perception of the water temperature. The brain then initiates a motor command by stimulating an upper motor neuron in the cerebral cortex. The axon of the upper motor neuron extends all the way to the spinal cord, where it synapses with a lower motor neuron in the gray matter of the spinal cord. The impulse then travels down the lower motor neuron back to the hand where it synapses with the skeletal muscles of the hand. This triggers the muscle contractions that turn the dials of the shower to adjust the water temperature.](https://substackcdn.com/image/fetch/$s_!x-HL!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3ce19781-7069-42d4-9d35-c62bd56bf76e_900x644.jpeg)](<https://substackcdn.com/image/fetch/$s_!x-HL!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3ce19781-7069-42d4-9d35-c62bd56bf76e_900x644.jpeg>)Nervous system components (figure from [here](<https://courses.lumenlearning.com/umd-publichealthbio/chapter/the-function-of-nervous-tissue/>)).

#### Training complexity

Related to the separation of concerns above, an end-to-end network must learn contact mechanics, actuator dynamics, delays, friction, impact stabilization, as well as task-level planning, all in one gradient signal.

This creates extremely long credit chains and high sample complexity. Hierarchical control factorizes the learning problem.

#### Feedback control loops; tactile and force feedback

With a fully end-to-end system, any feedback on how the executing is going can only come in at the top. In contrast, a dedicated low-level control unit can run its own feedback controller that performs stabilization functions. This is in effect what we saw above with the selection of the impedance controller in the Peng and Hutter papers above.

Secondly, a low-level controller also provides a great opportunity to incorporate a rich set of sensory signals such as tactile and force feedback information. Rodney Brooks underlines the importance of non-visual feedback in his [Sep 2025 essay](<https://rodneybrooks.com/why-todays-humanoids-wont-learn-dexterity/>), going as far as to flag it as a roadblock. The problem is, if you must have force feedback in an end-to-end model, you first have to contend with the lack of large-scale force data to train it from, as well as the much larger end-to-end model you now have to train and evaluate at inference-time. As I responded to a Substack comment [here](<https://substack.com/@avikde/note/c-203946866?r=5vzx85&utm_source=notes-share-action&utm_medium=web>), a low-level control unit is a potential way that that data could be incorporated, without increasing the dimensionality of the higher-level brain.

#### Control bandwidth

Real-world physics and dynamics don’t wait for end-to-end inference to complete, and most implementations (Physical Intelligence’s action chunking, Figure’s rate-decoupled system 1, etc.) need to decouple the control bandwidth of the cognitive layer from the low-level controller.

talks about this aspect as an action inference limitation in his excellent [post about VLA’s](<https://itcanthink.substack.com/p/vision-language-action-models-and>) which you should read if you haven’t.

#### Sim2real transfer

As discussed in my recent [world models post](<https://www.avikde.me/p/the-ai-world-models-debate-and-its>), almost all these implementations that utilize large-scale demonstration data need to follow it up with reinforcement learning post-training in simulation. This surfaces an issue that has been named “sim2real transfer,” where the simulator’s accuracy can limit the deployed behavior. This has a number of solutions including domain randomization and actuator networks, but alternatively, having a low-level controller can in many cases absorb modeling error with their inverse dynamics functionality. Physics errors affect torque-level policies massively, but impedance control, whole-body control, or model-predictive control absorb modeling error by actively driving mismatch errors to zero.

#### Safety constraints

We can explicitly add torque constraints, joint kinematic limits, self-collision avoidance, to a low-level controller. This is intuitively true, but I’ll leave an example of a [recent research paper](<https://umi-ft.github.io/>) which found out exactly this. Quoting the author:

> Introducing UMI-FT: the UMI gripper equipped with force/torque sensors (CoinFT) on each finger. Multimodal data from UMI-FT, combined with diffusion policy and compliance control, enables robots to apply sufficient yet safe force for task completion. 

[![](https://substackcdn.com/image/fetch/$s_!1u9p!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F72c63ff0-9c9d-4039-a248-06e4b600e33e_633x271.png)](<https://substackcdn.com/image/fetch/$s_!1u9p!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F72c63ff0-9c9d-4039-a248-06e4b600e33e_633x271.png>)UMI-FT [research paper](<https://umi-ft.github.io/>) architecture with explicity safety constraints in lower-level controllers.

#### Generalization across hardware embodiment (*maybe)

In principle, if the low-level controller completely abstracts the hardware, the higher-level brain’s functionality can be kept the same with different embodiments. Intuitively, you can reuse high-level policies if low-level layers abstract hardware, and you can improve low-level stability without retraining ML.

However, this intuitive point is difficult to verify due to the methodology of how the cognitive models are developed today. The end-to-end pixel → action policies always incorporate some amount of information about the embodiment, so it isn’t possible to train an abstract cognitive model. In practice, the foundation models of today train on [cross-embodiment](<https://www.pi.website/blog/pi0>) data to obtain generalizable knowledge. To get to the bottom of this facet, we would need to understand what constitutes a cognitive model separate from embodiment, and that is not known yet as discussed in my previous world models post:

### Closing thoughts

With the end of Sense-Plan-Act, the new robotics north star is an end-to-end pipeline that does away with the need for any task-specific pipeline architecture or programming. However, today’s successful implementations tell a different story, and there are a number of intuitive reasons for this.

Foundation models excel at semantic, perceptual, and strategic reasoning, but they are mismatched to high-bandwidth, stability-critical motor control. A robust robotic architecture separates concerns into layers aligned with physical timescales and modeling regimes.

In this (part 1) article, we focused on standard visuomotor task execution. In part 2 of this series, we’ll look at how unexpected events and motor adaptation are handled in these architectures. After that, to continue this series, I’d also like to explore a standalone demonstration that can be published as an open-source repo that examines a few of these architectures and compares them fairly.

If you found this post interesting, please let me know in the comments, and share, and subscribe. Thanks for reading!

[Leave a comment](<https://www.avikde.me/p/the-architecture-behind-end-to-end/comments>)

[Share](<https://www.avikde.me/p/the-architecture-behind-end-to-end?utm_source=substack&utm_medium=email&utm_content=share&action=share>)

Thanks for reading min{power}! Subscribe for free to receive new posts and support my work.
