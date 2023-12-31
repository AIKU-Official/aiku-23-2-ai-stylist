# AI Stylist

📢 2023년 2학기 [AIKU](https://github.com/AIKU-Official) 활동으로 진행한 프로젝트입니다
🎉 2023년 2학기 AIKU Conference 장려상 수상!

## 소개

**🤔 매일 아침 모두의 고민, “오늘 뭐 입지?”**

누구나 한 번쯤 했을 법한 생각이죠. **내 옷장 속의 아이템과 상황을 바탕으로 오늘의 코디를 추천** 받을 수 있다면 얼마나 좋을까요? 본 프로젝트는 이 고민거리를 해결하기 위한 딥러닝 모델을 만들어보고자 하는 생각으로부터 시작되었습니다.

## 방법론

<p align="center">
    <img src="./image/prob_formulation.png"
        alt="problem formulation"
        style="width: 70%">
</p>

### Task 1. Representation Learning

본 프로젝트에서는 좋은 특징을 두루 갖춘 FashionCLIP의 Pre-trained 모델을 패션 아이템 이미지를 임베딩하는 단계에 이용하였습니다.

> **FashionCLIP** [[repo]](https://github.com/patrickjohncyh/fashion-clip)
>
> _Proposed in [“Contrastive language and vision learning of general fashion concepts”](https://www.nature.com/articles/s41598-022-23052-9),
> Nature Scientific Reports_

- **Fashion domain:** 패션 도메인에 대해 사전 학습된 CLIP 모델
- **Representation:** 옷에 대한 좋은 Visual + Textual 지식을 가지고 있음
- **Multimodality:** 텍스트와 이미지 모두 사용 가능
- **Easy to Use:** 코드 사용성 좋음

### Task 2. Outfit Recommendation

프로젝트를 진행하며 다양한 구조와 손실 함수, 학습 테크닉을 시도했습니다. 그 중 주된 네 가지의 모델 구조를 소개합니다.

![timeline](./image/model_history.png)

#### End-to-End Architecture

<details>
<summary>FashionMLP</summary>
<div markdown="1">

![model](./image/fashionmlp.png)

</div>
</details>

<details>
<summary>Style-Aware Network</summary>
<div markdown="1">

![model](./image/StyleAwareNet.png)

</div>
</details>

#### Re-Ranking

<details>
<summary>Style-Agnostic Network</summary>
<div markdown="1">

![model](./image/StyleAgnosticNet.png)

</div>
</details>

<details>
<summary>Outfit Transformer</summary>
<div markdown="1">

</div>
</details>

## 환경 설정

### Requirements

```
cd ai-stylist
pip install -r requirements.txt
```

## 사용 방법

### Data Preparation

사용하는 데이터셋을 `./data` 에 두고 실행합니다. 여기(추후 추가 예정)에서 다운받을 수 있습니다.

### Training

> FashionMLP

```bash
cd ai-stylist/FashionMLP/recommender
python main.py
```

> StyleAwareNet

```bash
cd ai-stylist/StyleAwareNet/style_aware_net
python main.py
```

> StyleAgnosticNet

```bash
cd ai-stylist/StyleAgnosticNet/style_agnostic_net
python main.py
```

### Training

> StyleAwareNet

```bash
cd ai-stylist/FashStyleAwareNet
python demo.py
```

> StyleAgnosticNet

```bash
cd ai-stylist/StyleAgnosticNet
python demo2_{DATASET_NAME}.py
```

> OutfitTransformer

```bash
cd ai-stylist/OutfitTransformer
python rerank_items.py
```

## 예시 결과

### Style Aware Network

![result1](./image/result_styleawarenet.png)

### Re-ranking with Style Agnostic Network

![result2](./image/result_styleagnosticnet.png)

### Re-ranking with Outfit Transformer

![result3](./image/result_ot.png)

## 팀원

- [김채현](https://github.com/kchyun): Research, Data processing, Modeling (StyleAgnosticNet, Re-ranking)
- [김민영](https://github.com/EuroMinyoung186): Research, Data Crawling, Modeling (FashionMLP, Re-ranking)
- [김민재](https://github.com/kwjames98): Research, Experiments, Modeling (FashionMLP, StyleAwareNet, Re-ranking)
- [오원준](https://github.com/owj0421): Research, Data processing, Modeling (FashionMLP, StyleAwareNet, OutfitTransformer)
