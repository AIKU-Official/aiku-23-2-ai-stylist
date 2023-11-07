import torch
from transformers import CLIPProcessor, CLIPModel, CLIPVisionModelWithProjection, CLIPTextModelWithProjection, CLIPTokenizer
from typing import List, Tuple
import PIL


class FashionEmbeddingGenerator():
    """이미지 혹은 텍스트 배치를 받아 리스트형식의 CLIP Projection 임베딩으로 변환합니다."""
    def __init__(
            self,
            device: str='cuda', 
            pretrained_model_name: str='patrickjohncyh/fashion-clip'
            ):
        self.device = torch.device('cuda') if device == 'cuda' and torch.cuda.is_available() else torch.device('cpu')
        self.image_model = CLIPVisionModelWithProjection.from_pretrained(pretrained_model_name)
        self.text_model = CLIPTextModelWithProjection.from_pretrained(pretrained_model_name)
        self.processor = CLIPProcessor.from_pretrained(pretrained_model_name)
        self.tokenizer = CLIPTokenizer.from_pretrained(pretrained_model_name)

        self.image_model.to(self.device)
        self.image_model.eval()
        self.text_model.to(self.device)
        self.text_model.eval()

    @torch.no_grad()
    def img2embed(
        self, 
        images: List[PIL.Image.Image]
        ) -> List[List[float]]:
        inputs = self.processor(images=images, return_tensors="pt", padding=True)
        image_embeds = self.image_model(**inputs.to(self.device)).image_embeds.tolist()
        return image_embeds
    
    @torch.no_grad()
    def text2embed(
        self, 
        texts: List[str]
        ) -> List[List[float]]:
        inputs = self.tokenizer(text=texts, return_tensors="pt", padding=True)
        text_embeds = self.text_model(**inputs.to(self.device)).text_embeds.tolist()
        return text_embeds