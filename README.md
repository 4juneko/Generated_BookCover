# 아티커버
아티커버는 책 제목, 장르, 내용, 요구사항을 입력하면 그에 맞는 책표지를 생성해주는 Stable Diffusion 기반 프로젝트입니다.  

## 목차

- [기술적 목표](#기술적-목표)
- [구현 방법](#구현-방법)
- [요구 사항](#요구-사항)
- [팀원들](#팀원들)
- [참고](#참고)

## 기술적 목표

이 프로젝트에서 추구하는 기술적 목표는 명확합니다.  

**1. 다양한 비율의 책표지 이미지를 생성한다.**  

**2. 책표지에 포함된 제목을 왜곡없이 생성한다.**  

**3. 텍스트와 배경을 나누어 생성한다.**  

## 구현 방법


## 요구 사항


## 팀원들  

아티커버는 AI학교 AIFFEL 온라인 코어 3기 소속의 [한기혁](https://github.com/AIHyuck), [고주은](https://github.com/4juneko), [이호규](https://github.com/hogyu)가 2023년 6월 30일부터 2023년 8월 11일까지 진행하는 프로젝트입니다.  

팀원들은 각자의 도메인에서 활약하다가 AI를 공부하기 위해 모였고 이 프로젝트가 그 결실이자 그들의 새로운 시작입니다.

팀원들이 모두 같이 공부하고 나누고 실패하고 이겨내며 이 프로젝트를 발전시킵니다.

## 참고

[Hugging Face text to image - LoRA](https://github.com/huggingface/diffusers/blob/main/examples/text_to_image/README.md#training-with-lora)




---------
---------
# 아티커버
아티커버는 책 제목, 장르, 내용, 요구사항을 입력하면 그에 맞는 책표지를 생성해주는 Stable Diffusion 기반 프로젝트입니다.  

## 목차

- [기술적 목표](#기술적-목표)
- [관련 선행 기술](#관련-선행-기술)
- [프로젝트 흐름](#프로젝트_흐름)
- [구현 방법](#구현-방법)
- [요구 사항](#요구-사항)
- [팀원들](#팀원들)


## 기술적 목표
- 책내용에 적합한 이미지
    책의 제목과 내용에 어울리는 책표지를 생성함과 동시에 출판될 책의 크기를 고려해이미지를 원하는 비율의 이미지로 생성    
- 텍스트 편집    
    생성 이미지 모델에서 취약한 정확하지 않은 텍스트 생성을 극복하고자 알맞게 내용을 수정 가능하도록 함.    
- 적합한 해상도    
    이미지 생성 모델의 대부분 출력물은 512**512 or 1024**1024이다 하지만 인쇄하여 책을 출판하기 위해서는 보다 높은 해상도의 결과물이 필요하다
  
## 관련 선행 기술
- Book Cover Synthesis from the Summary(https://arxiv.org/abs/2211.02138)
   ![image](https://github.com/AIHyuck/Arti_Cover/assets/126551150/85f516ac-66d7-4921-aa46-64e7fe08231d)
   - Accepted as a full paper in AICCSA2022 (19th ACS/IEEE International Conference on Computer Systems and Applications)
   - StyleGAN, AttnGAN, DF-GAN, DALL-E 모델을 이용하여 책 표지 생성
   - 결과물이 어떤 내용의 책인지 알 수 없음.
   - ~25,000개의 데이터 셋
  - 마이크로소프트 디자이너
    ![image (2)](https://github.com/AIHyuck/Arti_Cover/assets/126551150/8d07f5c3-9efa-4fb1-bdf6-a200a7f42bdd)
    - 가장 목표치에 근접하는 생성 툴
    - 텍스트 또는 이미지를 input을 받아 이미지를 생성
    - 텍스트 위치 변경 및 내용 변경 가능
    - 이미지 비율은 지정 불가
    - 책표지보단 엽서 이미지 같은 사진도 많이 출력
    - 다른 탬플릿 또는 추가 이미지 부착 가능
    - 텍스트 위치 변경 및 내용 변경 가능
  - FontFits
    ![Untitled (1)](https://github.com/AIHyuck/Arti_Cover/assets/126551150/88deb045-dbeb-4429-8094-4477c414d90a)
    - 책 표지에 필요한 텍스트 생성
    - 20만개 이상의 dataset 필요
    - 복잡한 전처리 과정( 책 표지에서 텍스트 지우기, 마스크 제작 등)
    
## 프로젝트 흐름
![화면 캡처 2023-08-09 180730](https://github.com/AIHyuck/Arti_Cover/assets/126551150/4f5c87fd-55d3-4bb3-9fde-17f61a9e2ef0)

## 구현 방법
### Generate
- pretrained model로 Stable Diffusion-v-1-4를 사용하고 LoRA로 fine-tune
- Stable Diffusion  소개
    - 2022년에 출시된 딥 러닝, 텍스트-이미지 모델
    - 텍스트 설명에 따라 상세한 이미지를 생성하는 데 주로 사용
    - 인페인팅, 아웃페인팅, 이미지 생성과 같은 다른 작업에도 적용 가능
    - 코드 및 모델 가중치 공개됨.
    - 주제 변경이 용이 (Fine-tuning 이용)
    - 최소 8GB VRAM이 있는 일반 GPU에서 실행 가능

- LoRA (Low-Rank Adaptation of Large Language Models) 소개
    - 대규모 언어 모델을 미세 조정하는 문제를 해결하기 위해 도입된 기술
    - 미리 훈련된 모델 가중치와 각 트랜스포머 블록에서 주입 가능한 계층(순위 분해 행렬)을 동결할 것을 제안
        
        ⇒ 그레이디언트는 대부분의 모델 가중치에 대해 계산할 필요가 없기 때문에 훈련 가능한 매개 변수와 GPU 메모리 요구 사항의 수가 크게 감소함.
        
    - 언어 모델 뿐 아니라 다른 분야에도 적용 가능.
    - crossateention 블럭(노란색 부분)은 이미지와 텍스트 표현 사이의 관계를 구축
      ![latent-diffusion](https://github.com/AIHyuck/Arti_Cover/assets/126551150/f9ca4de3-5bec-4eb9-80aa-80d9ac426c8b)

    - 장점
        - 작은 데이터 셋 : 최소 필요 데이터 15~20개
        - 짧은 학습 시간 : 2시간30분 / 데이터 100개
        - 가벼운 학습 결과 파일 : ~ 3MB
        - 2080 Ti with 11GB VRAM

- Dataset
    - 데이터 수집 : 아마존 베스트 셀러 Top 20
    - SciFi, Children, Computer, Religion, Marvel Comics 분야 총 100개 수집
    - huggingface.co에 공유 JuneKo/bookCover_sciFi_child_com_reli_marvel
- LoRA 학습 후 결과 모델
    - Sci-Fi & Children
        - https://drive.google.com/drive/folders/1YQe07EJbcotzJM8TMQF_CySLSY0n3YpK?usp=sharing
    - Sci-Fi, Children, Computer, Religious, Marvel_comics
        - https://drive.google.com/drive/folders/1nSZ9pdZ3BFBoNQ-OhJK8A255WPUgi4nx?usp=sharing
- Reference
    
    https://medium.com/@bobi_29852/lora-keras-implementation-for-fine-tuning-stable-diffusion-1c3318da5ff7
    
    https://modulabs.co.kr/blog/stable-diffusion-ai/
    
    👍 https://jalammar.github.io/illustrated-stable-diffusion/
    
    https://aituts.com/stable-diffusion-lora/
    
    https://huggingface.co/blog/lora
    
    https://github.com/huggingface/diffusers/blob/main/examples/text_to_image/README.md#training-with-lora
---
### Edit Text
- 책 표지를 생성하면 이미지 생성 모델의 특징으로 의미 없는 유사 글자가 많들어져 텍스트 수정이 필요.
- SRNet, MOSTEL, SSTE, STEFANN, Imp2Font 등 Scene text editing Model을 시도하였으나 미리 학습된 DIffSTE 모델을 이용하기로 함.

- DiffSTE(Diffusion-based Scene Text Editing) 소개
    - 듀얼 인코더 디자인을 사용하여 그림에 있는 글자를 수정하는 목적으로 pretrained diffusion을 개선하기 위해 DiffSTE 모델이 만들어짐.
    - 문자 인코더와 스타일 제어를 위한 명령 인코더를 포함하는 듀얼 인코더 설계로 사전 훈련된 확산 모델을 개선한 후 지정된 스타일이나 주변 텍스트의 스타일을 배경으로 텍스트 명령에서 해당 이미지로의 매핑을 학습
     ![Untitled (1)](https://github.com/AIHyuck/Arti_Cover/assets/126551150/fdd2b32f-2d3e-4e16-9218-2476df6ce988)
  
    - Dataset
        - the synthetic dataset (Synthetic)
            and three real-world datasets (ArT[9], COCOText[13], and TextOCR [44]) for instruction tuning.
        - 100 font families from the google fonts library2
            and 954 XKCD colors3 for text rendering
        - randomly select 200 images for validation and 1000 images for testing from each dataset.
    
    - DiffSTE를 이용하기 위한 Input
        - All the images are cropped/resized to 256×256 resolution
        - 새로운 텍스트가 들어갈 마스크
        - 새로운 텍스트
    
    - DiffSTE의 결과물
       ![Untitled (2)](https://github.com/AIHyuck/Arti_Cover/assets/126551150/5af8e934-51e1-4772-81a2-1bcc8447aaee)

- Reference
    - https://github.com/UCSB-NLP-Chang/DiffSTE
    - https://arxiv.org/pdf/2304.05568.pdf
---
### Remove Text
- 생성한 책 표지의 유사 글자들이 필요보다 많아 지워야 하는 과정이 필요
- Detextify에서 힌트를 얻어 Keras-OCR로 문자를 인식하고 그 부분을 Stable Diffusion Inpainting으로 그림의 배경을 참고하여 문자 있던 부분을 채워 넣음.
- Keras-OCR 소개
    - 이미지 속 영문을 bounding-box로 찾고, 어떤 텍스트가 포함되는지 알 수 있음.
    - 텍스트의 위치를 찾아내는 것은 segmentation 기반으로 함.
    - 
- Stable Diffusion Inpainting 소개
    - Stable Diffusion Inpainting-v-1-2의 가중치를 초기화 ⇒ 595k steps의 평이한 학습 ⇒ 440k steps의 inpainting을 학습
    
- Reference
    - [GitHub - faustomorales/keras-ocr: A packaged and flexible version of the CRAFT text detector and Keras CRNN recognition model.](https://github.com/faustomorales/keras-ocr)
    - https://github.com/iuliaturc/detextify
    - [runwayml/stable-diffusion-inpainting · Hugging Face](https://huggingface.co/runwayml/stable-diffusion-inpainting)
---
### Upscale
- 출판업계에서는 보통 A4 기준 300dpi(2,480*3,508)를 이용하는데 결과물의 해상도 256*256 해상도를 높일 필요가 있어 Real-ESRGAN을 이용함.
- Real-ESRGAN 소개
    
    ![Untitled (3)](https://github.com/AIHyuck/Arti_Cover/assets/126551150/eaaba7fc-5d3f-401a-8084-bfebbbee6064)
    
    - 4배로 해상도를 높일 수 있음.
        ![Untitled (4)](https://github.com/AIHyuck/Arti_Cover/assets/126551150/d60cb74f-f0a8-4f2c-b843-fd9c97b4a2ff)
        
        
    - 
- Reference
    - [arxiv.org/pdf/2107.10833.pdf](https://arxiv.org/pdf/2107.10833.pdf)
    - [GitHub - xinntao/Real-ESRGAN: Real-ESRGAN aims at developing Practical Algorithms for General Image/Video Restoration.](https://github.com/xinntao/Real-ESRGAN)
 
## 요구 사항

## 팀원들  

아티커버는 AI학교 AIFFEL 온라인 코어 3기 소속의 [한기혁](https://github.com/AIHyuck), [고주은](https://github.com/4juneko), [이호규](https://github.com/hogyu)가 2023년 6월 30일부터 2023년 8월 11일까지 진행하는 프로젝트입니다.  

팀원들은 각자의 도메인에서 활약하다가 AI를 공부하기 위해 모였고 이 프로젝트가 그 결실이자 그들의 새로운 시작입니다.

팀원들이 모두 같이 공부하고 나누고 실패하고 이겨내며 이 프로젝트를 발전시킵니다.
