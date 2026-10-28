# CMU 11-868 — Large Language Model Systems (Fall 2026)

A local archive of the **official** course materials for Carnegie Mellon University's
[11-868 Large Language Model Systems](https://llmsystem.github.io/llmsystem2026fall/).

> Every item below is sourced from, and links back to, the official course website:
> **<https://llmsystem.github.io/llmsystem2026fall/>** and the official assignment site
> **<https://llmsystem.github.io/llmsystemhomework/>**.
>
> Archived on **2026-09-19**. The course site is live and may change — always treat the
> official pages as the source of truth.

---

## Course at a Glance

| | |
|---|---|
| **School** | Carnegie Mellon University |
| **Course** | 11-868, Large Language Model Systems |
| **Term** | Fall 2026 |
| **Instructor** | [Lei Li](https://www.cs.cmu.edu/~leili/) |
| **Lectures** | Monday & Wednesday, 5:00–6:20pm, POS A35 |
| **Recitations** | Friday, 12:30–1:50pm, DH A302 |
| **Home** | <https://llmsystem.github.io/llmsystem2026fall/> |

The course covers the "hardware architectures, software stacks, and system techniques
required to design, implement, and improve next-generation LLM systems" — distributed
training, GPU/TPU acceleration, serving engines, and optimization techniques.
(Source: [course home](https://llmsystem.github.io/llmsystem2026fall/).)

### Teaching Assistants

- [Yuheng Ding](http://aaxding.github.io/)
- [Rishiraj Nagarajan](https://www.linkedin.com/in/rishirajn/)
- Jie Ren
- [Aditya Tummala](https://www.linkedin.com/in/adi-tummala/)
- [Sreeram Vennam](https://vnnm404.github.io/)
- [Mira Xiao](https://www.linkedin.com/in/min-mira-xiao-4884971a7/)

### Grading

| Component | Weight |
|---|---|
| Homework | 44% |
| Project (proposal 2% · mid-term 2% · presentation 20% · final report 20%) | 44% |
| Quiz | 10% |
| Participation | 2% (+ up to 2% bonus) |

Late policy: "Each late day will incur 30% discount on the grades."
Source: [Logistics](https://llmsystem.github.io/llmsystem2026fall/docs/Logistics).

---

## Official Course Pages

| Page | Official URL | Local snapshot |
|---|---|---|
| Home | <https://llmsystem.github.io/llmsystem2026fall/> | [`docs/00-home.html`](docs/00-home.html) |
| Logistics | <https://llmsystem.github.io/llmsystem2026fall/docs/Logistics> | [`docs/01-logistics.html`](docs/01-logistics.html) |
| Syllabus | <https://llmsystem.github.io/llmsystem2026fall/docs/Syllabus> | [`docs/02-syllabus.html`](docs/02-syllabus.html) |
| Projects | <https://llmsystem.github.io/llmsystem2026fall/docs/Projects> | [`docs/03-projects.html`](docs/03-projects.html) |
| FAQ | <https://llmsystem.github.io/llmsystem2026fall/docs/FAQ> | [`docs/04-faq.html`](docs/04-faq.html) |
| Homework index | <https://llmsystem.github.io/llmsystemhomework/> | [`docs/10-homework-index.html`](docs/10-homework-index.html) |
| Assignment 1 | <https://llmsystem.github.io/llmsystemhomework/assignment_1/> | [`docs/11-assignment_1.html`](docs/11-assignment_1.html) |
| Assignment 2 | <https://llmsystem.github.io/llmsystemhomework/assignment_2/> | [`docs/12-assignment_2.html`](docs/12-assignment_2.html) |
| Assignment 3 | <https://llmsystem.github.io/llmsystemhomework/assignment_3/> | [`docs/13-assignment_3.html`](docs/13-assignment_3.html) |
| Assignment 4 | <https://llmsystem.github.io/llmsystemhomework/assignment_4/> | [`docs/14-assignment_4.html`](docs/14-assignment_4.html) |
| Assignment 5 | <https://llmsystem.github.io/llmsystemhomework/assignment_5/> | [`docs/15-assignment_5.html`](docs/15-assignment_5.html) |
| Assignment 6 | <https://llmsystem.github.io/llmsystemhomework/assignment_6/> | [`docs/16-assignment_6.html`](docs/16-assignment_6.html) |
| Assignment 7 | <https://llmsystem.github.io/llmsystemhomework/assignment_7/> | [`docs/17-assignment_7.html`](docs/17-assignment_7.html) |

---

## Official Code Repositories (cloned into `repos/`)

All repositories below are the **official starter code** published by the course staff under
the [`llmsystem`](https://github.com/llmsystem) GitHub organization, and each is linked from
its corresponding page on <https://llmsystem.github.io/llmsystemhomework/>.

| Local path | Upstream | Linked from |
|---|---|---|
| [`repos/llmsys_hw1`](repos/llmsys_hw1) | <https://github.com/llmsystem/llmsys_hw1> | [Assignment 1](https://llmsystem.github.io/llmsystemhomework/assignment_1/) |
| [`repos/llmsys_hw2`](repos/llmsys_hw2) | <https://github.com/llmsystem/llmsys_hw2> | [Assignment 2](https://llmsystem.github.io/llmsystemhomework/assignment_2/) |
| [`repos/llmsys_hw3`](repos/llmsys_hw3) | <https://github.com/llmsystem/llmsys_hw3> | [Assignment 3](https://llmsystem.github.io/llmsystemhomework/assignment_3/) |
| [`repos/llmsys_hw4`](repos/llmsys_hw4) | <https://github.com/llmsystem/llmsys_hw4> | [Assignment 4](https://llmsystem.github.io/llmsystemhomework/assignment_4/) |
| [`repos/llmsys_hw5`](repos/llmsys_hw5) | <https://github.com/llmsystem/llmsys_hw5> (the assignment page still links the old name `llmsys_f25_hw5`, which GitHub redirects) | [Assignment 5](https://llmsystem.github.io/llmsystemhomework/assignment_5/) |
| [`repos/llmsys_hw6`](repos/llmsys_hw6) | <https://github.com/llmsystem/llmsys_hw6> | [Assignment 6](https://llmsystem.github.io/llmsystemhomework/assignment_6/) |
| [`repos/llmsys_hw7`](repos/llmsys_hw7) | <https://github.com/llmsystem/llmsys_hw7> | [Assignment 7](https://llmsystem.github.io/llmsystemhomework/assignment_7/) |
| [`repos/llmsys_code_examples`](repos/llmsys_code_examples) | <https://github.com/llmsystem/llmsys_code_examples> | [Assignment 1 — CUDA demo](https://llmsystem.github.io/llmsystemhomework/assignment_1/) |

Re-clone them yourself with:

```bash
cd repos
for i in 1 2 3 4 5 6 7; do git clone "https://github.com/llmsystem/llmsys_hw$i.git"; done
git clone https://github.com/llmsystem/llmsys_code_examples.git
```

---

## Assignments

The assignments build **miniTorch**, a teaching deep-learning framework originally created by
[Prof. Sasha Rush](https://rush-nlp.com/) and extended by the course staff with CUDA kernels
and GPU optimizations. Source: [assignment site](https://llmsystem.github.io/llmsystemhomework/).

### [Assignment 1 — CUDA Programming](https://llmsystem.github.io/llmsystemhomework/assignment_1/)
Implement CUDA kernels for tensor ops and wire them into miniTorch: Map (15), Zip (25),
Reduce (25), Matrix Multiplication (30), Integration Test (5).
Code in `src/combine.cu`, bound through `minitorch/cuda_kernel_ops.py`.
- Repo: <https://github.com/llmsystem/llmsys_hw1>
- [PSC account guide](https://docs.google.com/document/d/1FzNWon1GePQNCqjx3tiXU-FQtxeBDruvjwORWRHhoVs/edit?usp=sharing)
- [uv — getting started](https://docs.astral.sh/uv/getting-started)
- [CUDA acceleration demo](https://github.com/llmsystem/llmsys_code_examples/tree/main/cuda_acceleration_demo)
- [NVIDIA reduction paper](https://developer.download.nvidia.com/assets/cuda/files/reduction.pdf)

### [Assignment 2 — miniTorch Framework](https://llmsystem.github.io/llmsystemhomework/assignment_2/)
Autodiff (`topological_sort`, `backpropagate`) — 40 pts; `Linear` / `Network` modules — 30 pts;
`binary_cross_entropy_loss` + training loop — 30 pts. Target ≥75% validation accuracy on SST-2.
- Repo: <https://github.com/llmsystem/llmsys_hw2>

### [Assignment 3 — Transformer Architecture](https://llmsystem.github.io/llmsystemhomework/assignment_3/)
Decoder-only GPT-2-style transformer in miniTorch, trained on IWSLT14 De–En.
Tensor functions (20), basic modules (20), transformer (40), MT pipeline (20).
Target BLEU ≈ 20 ± 2; ~10+ hours of training.
- Repo: <https://github.com/llmsystem/llmsys_hw3>
- [Language Models are Unsupervised Multitask Learners](https://paperswithcode.com/paper/language-models-are-unsupervised-multitask)
- [On Layer Normalization in the Transformer Architecture](https://arxiv.org/pdf/2002.04745.pdf)

### [Assignment 4 — Transformer CUDA Acceleration](https://llmsystem.github.io/llmsystemhomework/assignment_4/)
LightSeq-style fused kernels: Softmax fwd/bwd (40), LayerNorm fwd/bwd (40), integration (20).
Target speedups ~6.5×, ~5.5×, ~15.8×, ~3.7×; end-to-end ~1.1×.
- Repo: <https://github.com/llmsystem/llmsys_hw4>

### [Assignment 5 — Distributed Training and Parallelism](https://llmsystem.github.io/llmsystemhomework/assignment_5/)
Data parallel (50) and pipeline parallel (50) for GPT-2, using only `torch.distributed` and
`torch.multiprocessing.Process`. Target ≥1.5× speedup on 2 GPUs.
- Repo: <https://github.com/llmsystem/llmsys_hw5>
- [PSC usage guide](https://docs.google.com/document/d/1FzNWon1GePQNCqjx3tiXU-FQtxeBDruvjwORWRHhoVs/edit?usp=sharing)

### [Assignment 6 — Advanced Training and Inference Systems](https://llmsystem.github.io/llmsystemhomework/assignment_6/)
DeepSpeed ZeRO + LoRA fine-tuning of LLaMA-2 7B on 2×V100 (50); SGLang inference with
RadixAttention (50). Requires sm75+ GPUs for SGLang.
- Repo: <https://github.com/llmsystem/llmsys_hw6>
- [meta-llama/Llama-2-7b-hf](https://huggingface.co/meta-llama/Llama-2-7b-hf)

### [Assignment 7 — Introduction to RLHF](https://llmsystem.github.io/llmsystemhomework/assignment_7/)
Build a VERL-like RLHF stack: ranking loss + reward model (40), `VERLTrainer` (40),
evaluation (20), on `Anthropic/hh-rlhf`.
- Repo: <https://github.com/llmsystem/llmsys_hw7>
- [VERL documentation](https://verl.readthedocs.io/en/latest/)
- [HybridFlow paper](https://arxiv.org/abs/2409.19256)
- [Hugging Face RLHF blog](https://huggingface.co/blog/rlhf)
- [OpenAI PPO](https://openai.com/research/openai-baselines-ppo)

---

## Syllabus, Slides and Readings

All slide decks are mirrored in [`slides/`](slides) from
<https://llmsystem.github.io/llmsystem2026fall/docs/Syllabus>.

| Date | Topic | Slides (local) | Readings |
|---|---|---|---|
| 8/24 | Introduction to LLM | [01](slides/llmsys-01-intro.pdf) | — |
| 8/26 | GPU Programming Basics 1 | [02](slides/llmsys-02-gpu-programming.pdf) | [PMPP 4th Ed, ch. 2–4](https://learning.oreilly.com/library/view/programming-massively-parallel/9780323984638/?sso_link=yes&sso_link_from=cmu-edu) |
| 8/28 | Recitation 1: PSC, CUDA demo, HW1 | [google slides](https://docs.google.com/presentation/d/1v5IT8XZeWZ4FIlQzRLmEfcZv-kmfAyBIFyqYJkR5Lk8/edit?usp=sharing) | — |
| 8/31 | GPU Acceleration | [03](slides/llmsys-03-gpu-acceleration.pdf) | [PMPP ch. 5–6](https://learning.oreilly.com/library/view/programming-massively-parallel/9780323984638/?sso_link=yes&sso_link_from=cmu-edu) |
| 9/2 | DL Frameworks & Auto Differentiation · **HW1 due** | [04](slides/llmsys-04-dlframework.pdf) | [TensorFlow](https://www.usenix.org/system/files/conference/osdi16/osdi16-abadi.pdf) · [AutoDiff survey](https://arxiv.org/abs/1502.05767) · [Differentiable Programming](https://arxiv.org/abs/2403.14606) |
| 9/4 | Recitation 2: HW2, MiniTorch, more GPU | — | — |
| 9/9 | LLM Architecture & Pre-training · **HW2 due** | [05](slides/llmsys-05-LLM-architecture.pdf) | [Attention Is All You Need](https://arxiv.org/abs/1706.03762) · [DeepSeek-V2](https://arxiv.org/abs/2405.04434) · [GPT-3](https://arxiv.org/abs/2005.14165) |
| 9/11 | Recitation 3: Annotated Transformers | — | [The Annotated Transformer](https://nlp.seas.harvard.edu/annotated-transformer/) |
| 9/14 | Tokenization and Embedding | [06](slides/llmsys-06-tokenization.pdf) | [BPE](https://aclanthology.org/P16-1162/) · [SentencePiece](https://aclanthology.org/D18-2012/) · [VOLT](https://aclanthology.org/2021.acl-long.571/) |
| 9/16 | Generation & Speculative Decoding · **Project team due** | [07](slides/llmsys-07-decoding.pdf) | [Speculative Decoding](https://proceedings.mlr.press/v202/leviathan23a/leviathan23a.pdf) |
| 9/18 | Recitation 4: Tokens and Decoding | [google slides](https://docs.google.com/presentation/d/12GC-OW55eIX59W-DSfSQ0MPbVD8vQqG0/edit?usp=sharing&ouid=106741546184784039741&rtpof=true&sd=true) | — |
| 9/21 | Accelerating Transformer on GPU I | [08](slides/llmsys-08-transformer-acc.pdf) | [arXiv:2010.13887](https://arxiv.org/abs/2010.13887) |
| 9/23 | Accelerating Transformer on GPU II · **HW3 due** | [08](slides/llmsys-08-transformer-acc.pdf) | [arXiv:2110.05722](https://arxiv.org/abs/2110.05722) |
| 9/25 | Recitation 5: LightSeq demo | — | — |
| 9/28 | Guest (Srinath Mandalapu, Google): TPU and JAX | [10](slides/llmsys-10-JAX-XLA-TPU.pdf) | — |
| 9/30 | Guest (Srinath Mandalapu, Google): Pallas & Splash Attention · **Proposal due** | [11](slides/llmsys-11-pallas-splash-attention.pdf) | — |
| 10/2 | Recitation 6: JAX and TPU | — | — |
| 10/5 | Distributed Data Parallel Training | [12](slides/llmsys-12-data-parallel-training.pdf) | [PyTorch DDP (VLDB)](https://www.vldb.org/pvldb/vol13/p3005-li.pdf) |
| 10/7 | Model Parallel Training · **HW4 due** | [13](slides/llmsys-13-model-parallel.pdf) | [GPipe](https://arxiv.org/abs/1811.06965) · [Megatron-LM](https://arxiv.org/abs/2104.04473) |
| 10/9 | Recitation 7: Distributed training | — | — |
| 10/12 | Break | — | — |
| 10/19 | Systems for Mixture-of-Expert Models | [14](slides/llmsys-14-MoE.pdf) | [GShard](https://openreview.net/forum?id=qrwe7XHTmYb) · [Switch Transformer](https://arxiv.org/abs/2101.03961) · [DeepSpeed-MoE](https://arxiv.org/pdf/2201.05596.pdf) · [DeepSeek-MoE](https://arxiv.org/abs/2401.06066) |
| 10/21 | Memory Optimization in Distributed Training | [15](slides/llmsys-15-zero.pdf) | [ZeRO](https://arxiv.org/pdf/1910.02054.pdf) |
| 10/23 | Recitation 8: MoE | — | — |
| 10/26 | Model Quantization · **HW5 due** | [16](slides/llmsys-16-quantization.pdf) | [NN Quantization](https://arxiv.org/abs/2106.08295) · [AdaQuant](https://arxiv.org/abs/2006.10518) · [LLM.int8()](https://arxiv.org/abs/2208.07339) |
| 10/28 | Model Quantization II | [17](slides/llmsys-17-quantization2.pdf) | [GPTQ](https://arxiv.org/abs/2210.17323) |
| 10/30 | Recitation 9: Quantization | — | — |
| 11/2 | Efficient Fine-tuning for Large Models | [18](slides/llmsys-18-peft.pdf) | [CIAT](https://arxiv.org/abs/2104.08154) · [LoRA](https://arxiv.org/abs/2106.09685) · [QLoRA](https://arxiv.org/abs/2305.14314) |
| 11/4 | Optimizing Attention for Modern Hardware (Tri Dao) · **Mid-term report due** | [19](slides/llmsys-19-FlashAttention.pdf) | [FlashAttention](https://arxiv.org/pdf/2205.14135.pdf) · [FA2](https://arxiv.org/abs/2307.08691) · [FA3](https://arxiv.org/abs/2407.08608) · [FA4](https://arxiv.org/abs/2603.05451) |
| 11/6 | Recitation 10: LoRA and FlashAttention | — | — |
| 11/9 | LLM Serving with SGLang | [20](slides/llmsys-20-llm-serving-radixattention.pdf) | [ORCA](https://www.usenix.org/system/files/osdi22-yu.pdf) · [SGLang](https://arxiv.org/abs/2312.07104) |
| 11/11 | Efficient LLM Inference with PagedAttention / vLLM (Woosuk Kwon) | [21](slides/llmsys-21-vLLM.pdf) | [vLLM](https://arxiv.org/abs/2309.06180) |
| 11/13 | Recitation 11: SGLang and vLLM · **HW6 due** | — | — |
| 11/16 | Acceleration on TPU 1 | — | — |
| 11/18 | Acceleration on TPU 2 | — | — |
| 11/20 | Recitation 12: TPU acceleration | — | — |
| 11/23 | Efficient RL System for LLMs | — | [arXiv:2406.14088](https://arxiv.org/abs/2406.14088) |
| 11/30 | Serving with Disaggregated Prefill–Decoding · **HW7 due** | [25](slides/llmsys-25-dynamo.pdf) | [DistServe](https://arxiv.org/abs/2401.09670) |
| 12/2 | Better KV Cache for LLM Serving (Junchen Jiang) | [26](slides/llmsys-26-LMCache.pdf) | [CacheGen](https://arxiv.org/abs/2310.07240) · [CacheBlend](https://arxiv.org/abs/2405.16444) |
| 12/4 | Final project presentation | — | — |
| 12/6 | Final report due | — | — |

### Additional topics (date TBD)

| Topic | Slides (local) | Readings |
|---|---|---|
| DistServe: Disaggregated Prefill–Decode (Hao Zhang) | [29](slides/llmsys-29-disaggregating-prefill-decode.pdf) | [DistServe](https://arxiv.org/abs/2401.09670) |
| App Stack and Model Serving | [30](slides/llmsys-30-serving.pdf) | [Triton Inference Server](https://developer.nvidia.com/triton-inference-server) · [LightLLM](https://github.com/ModelTC/LightLLM) (the exact doc path cited by the syllabus, `.../blob/main/docs/LightLLM.md`, now 404s upstream) |
| LLM Serving on Heterogeneous Hardware | [28](slides/llmsys-28-mooncake-kTransformer.pdf) | [Mooncake](https://arxiv.org/abs/2407.00079) · [kTransformer](https://dl.acm.org/doi/10.1145/3731569.3764843) |
| Triton for Kernel Optimization | — | [Triton (MLSys'18)](https://mlsys.org/Conferences/doc/2018/146.pdf) |
| Retrieval-augmented Language Models | — | [RAG](https://arxiv.org/abs/2005.11401) |
| Nearest Vector Search for Embeddings | — | [HNSW](https://arxiv.org/abs/1603.09320) |
| Multimodal LLMs | — | [Flamingo](https://arxiv.org/abs/2204.14198) |
| Efficient Streaming LMs with Attention Sinks | — | [StreamingLLM](https://arxiv.org/abs/2309.17453) |

### Textbook

- *Programming Massively Parallel Processors*, 4th Ed. —
  [O'Reilly (CMU SSO)](https://learning.oreilly.com/library/view/programming-massively-parallel/9780323984638/?sso_link=yes&sso_link_from=cmu-edu).
  The FAQ calls it "the best resource for GPU CUDA programming."

---

## Course Project

Teams of 2–3. Either extend MiniTorch with scalable/accelerated LLM components by
reimplementing a recent LLM systems paper, or pursue new research aimed at MLSys / OSDI /
SOSP / SC. Source: [Projects](https://llmsystem.github.io/llmsystem2026fall/docs/Projects).

**Deliverables:** proposal → mid-term report (~6 pages) → final presentation → final report (~8 pages).

**Suggested MiniTorch components:** FlashAttention, PagedAttention, mixed-precision training,
LightSeq memory optimization, DPO training.

**Suggested research directions:** multimodal LLM training/inference, federated training,
quantized training/finetuning, biology/chemistry model optimization, browser-based LLM
inference, MoE scaling, heterogeneous hardware training, joint retrieval–LLM training,
KV cache management.

**Resources linked from the Projects page:**
- [MLSys 2024 LaTeX style](https://media.mlsys.org/Conferences/MLSYS2024/Styles/mlsys2024style.zip)
- <https://arxiv.org/abs/2010.13887>
- <https://openreview.net/forum?id=Kg0IDQF3wp&noteId=v5OYKJ2sra>
- <https://arxiv.org/abs/2411.11217>
- <https://arxiv.org/abs/2211.15841>
- <https://arxiv.org/abs/2404.12457>
- <https://arxiv.org/abs/2510.09665>
- <https://arxiv.org/abs/2407.00079>
- <http://arxiv.org/pdf/2312.07104>

---

## Layout of this archive

```
90_resources/courses/cmu/11_868_llm_systems/
├── README.md     ← this file
├── docs/         ← HTML snapshots of every official course page
├── slides/       ← 25 lecture PDFs from the official Syllabus page
└── repos/        ← git clones of the 8 official llmsystem repos
```

Total size: ~618 MB (89 MB slides, 529 MB repos — `llmsys_hw3` and `llmsys_code_examples`
carry large data/asset histories).

Each directory under `repos/` is a full git clone with its own `.git`. If you commit this
archive into a parent repository, git will record them as embedded repositories rather than
tracking their contents — convert them to submodules, or add `90_resources/courses/**/repos/` to your
`.gitignore` and re-clone with the loop above.

---

## Attribution

All course content, slides, assignments, and starter code are the property of the
**11-868 course staff at Carnegie Mellon University** and are reproduced here only as a
personal study mirror. Canonical sources:

- Course website — <https://llmsystem.github.io/llmsystem2026fall/>
- Assignment website — <https://llmsystem.github.io/llmsystemhomework/>
- GitHub organization — <https://github.com/llmsystem>
- Instructor — [Lei Li, CMU](https://www.cs.cmu.edu/~leili/)
- miniTorch, the framework the assignments build on, originates with
  [Prof. Sasha Rush](https://rush-nlp.com/) ([minitorch.github.io](https://minitorch.github.io/))

Per the [Logistics page](https://llmsystem.github.io/llmsystem2026fall/docs/Logistics),
sharing specific assignment solutions constitutes cheating. If you are currently enrolled,
use the community repositories below for orientation only — not for answers.

---

## Community Learning Repositories

Third-party repositories in which people recorded how they worked through this course.
These are **not official** and are not endorsed by the course staff — they are listed only as
study companions to the official material above. Star counts and last-push dates were verified
against the GitHub API on **2026-09-19**.

Ordered best-first, by how much of a genuine *learning record* each one is (notes, debugging
write-ups, incremental history) rather than by star count.

### Full-course solutions with written notes

- [mindorigin150/cmu11868](https://github.com/mindorigin150/cmu11868) — The strongest all-round record: HW1–HW7 plus lecture code examples over 103 commits, and a README of real debugging findings (a gradient-init bug that silently breaks HW3, a CUDA `gridDim` ordering fix, a `pycuda.autoinit` replacement). Links out to the author's own notes at `blog.mindorigin.top/AI/llmsys`. (⭐23, last push 2025-08-28)
- [HlinForest/llmsys-lab](https://github.com/HlinForest/llmsys-lab) — Chinese-language learning record: per-assignment write-ups for HW1–HW7 under `assignments/hw01..hw07` (题目梳理 + 实现笔记), plus a complete final project — "MiniTorch Memory-Efficient Inference with Paged KV Cache" — with a `docs/` proposal and report, benchmarks, and a reproducible `run_all.py`. (⭐0, last push 2026-09-06)
- [appleweiping/cmu11868-llm-systems](https://github.com/appleweiping/cmu11868-llm-systems) — An independent from-scratch reimplementation of the whole stack (autodiff, GPT-2 decoder, fused softmax/LayerNorm, DDP + GPipe on `torch.distributed`, KV-cache, int8/int4 quantization, LoRA), CPU-verified with measured result tables. Reads as much like a write-up as a solution set. (⭐0, last push 2026-07-04)
- [ztzhu1/CMU-11868](https://github.com/ztzhu1/CMU-11868) — Complete HW1–HW7, explicitly CUDA-focused (map/reduce kernels, tiled matmul, custom Softmax/LayerNorm forward+backward, autodiff); the README explains what each piece teaches. (⭐1, last push 2026-01-19)

### Full-course solutions, lighter on prose

- [QuangHuy54/CMU_11868_LLM_Systems_2025_Solutions](https://github.com/QuangHuy54/CMU_11868_LLM_Systems_2025_Solutions) — All seven assignments organized under descriptive names, each shipping a `setup_env_google_colab.sh` so they can be run without a local GPU. (⭐0, last push 2026-04-15)
- [SCPZ24/CMU11868Labs](https://github.com/SCPZ24/CMU11868Labs) — HW1–HW5 across 108 commits, so the incremental work history is intact even though there are no written notes. (⭐0, last push 2026-03-18)
- [Farewell2006/LLMSys](https://github.com/Farewell2006/LLMSys) — F25 HW1–HW5 with a dated changelog README recording per-assignment test status and the exact `tensor_functions.py` `View.backward` contiguity patch needed to pass HW3. (⭐1, last push 2026-04-16)
- [sa3kura/CMU11-868](https://github.com/sa3kura/CMU11-868) — HW1–HW5 with a Chinese README summarizing what each assignment builds (自动微分框架 + 手写 CUDA 算子, GPT-2 结构, Softmax/LayerNorm CUDA 优化). Useful as a roadmap in Chinese. (⭐0, last push 2026-07-03)
- [khubishah/cmu-11868-llm-systems](https://github.com/khubishah/cmu-11868-llm-systems) — F25 HW1–HW5 plus a `Resources/` folder of collected course material. (⭐1, last push 2025-11-18)
- [Light-yzc/CMU-11868](https://github.com/Light-yzc/CMU-11868) — Full F25 HW1–HW7; complete, but committed as a single dump with no notes. (⭐0, last push 2025-10-02)
- [FZYsheep/cmu11868](https://github.com/FZYsheep/cmu11868) — Full F25 HW1–HW7 plus an `images/` folder of result screenshots; single-commit dump. (⭐0, last push 2025-09-23)
- [owenk3/CMU-LLMSystem](https://github.com/owenk3/CMU-LLMSystem) — Spring-2025 `llmsys_s25_hw1`–`hw5` solutions. (⭐1, last push 2025-05-25)

### Earlier course versions and single assignments

- [pinqian77/11-868-llmsys-24s](https://github.com/pinqian77/11-868-llmsys-24s) — Spring-2024 HW1–HW4, with a README that walks through each assignment's sub-tasks. The cleanest description of the older four-assignment structure. (⭐2, last push 2024-04-03)
- [zhiblll/CMU_11_868](https://github.com/zhiblll/CMU_11_868) — HW1 only, but ships the whole worked miniTorch package plus a README reproducing the spec and environment setup — a handy HW1 reference build. (⭐0, last push 2026-03-09)
- [Riyabelle25/llmsys_f25_hw1](https://github.com/Riyabelle25/llmsys_f25_hw1) — HW1 only; the single starter-repo fork with any traction. (⭐1, last push 2025-08-25)

### Course projects (examples of the final deliverable)

- [aalexchengg/11868_final_project](https://github.com/aalexchengg/11868_final_project) — The most-starred community project repo for this course. (⭐3, last push 2025-04-29)
- [tantansir/RAGCachePlusPlus](https://github.com/tantansir/RAGCachePlusPlus) — Spring-2026 final project: cache-aware document ordering for low-latency RAG serving. (⭐2, last push 2026-04-24)
- [mistyreed63849/llmsys_project](https://github.com/mistyreed63849/llmsys_project) — FlashAttention and PagedAttention implemented on top of the course's miniTorch. (⭐0, last push 2026-05-01)

### Adjacent prep material

- [AlexGeControl/ECE408-Applied-Parallel-Programming](https://github.com/AlexGeControl/ECE408-Applied-Parallel-Programming) — Not 11-868 itself; the author frames it as CUDA preparation *for* this course. Worth a look if HW1's CUDA is the bottleneck. (⭐2, last push 2025-07-16)

### Other official `llmsystem` repos not cloned above

Beyond the current starter set, the [`llmsystem` org](https://github.com/llmsystem) also keeps
per-semester archives useful for diffing how assignments evolved, and the site source itself:

- `llmsys_s24_hw1`–`hw4` (Spring 2024; several archived) and `llmsys_s25_hw1`–`hw5` (Spring 2025)
- [llmsystem/llmsystem.github.io](https://github.com/llmsystem/llmsystem.github.io) — the Docusaurus source of the course website (⭐6)

### Ruled out during the search

- `wufeng15226/llmsys_s24_hw` — empty repository (0 KB).
- `Santhoshkumar-p/llmsystem2024spring` — a copy of the course site, not a personal learning record.
- The 56 forks of `llmsys_hw1` and 101 forks of `llmsys_s24_hw1` are almost entirely zero-star student forks with no notes.
- No standalone Chinese-language notes repo (知乎-style) surfaced beyond the two listed above; [csdiy.wiki's 11-868 page](https://csdiy.wiki/en/%E6%B7%B1%E5%BA%A6%E7%94%9F%E6%88%90%E6%A8%A1%E5%9E%8B/%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/CMU11-868/) links only official material.

