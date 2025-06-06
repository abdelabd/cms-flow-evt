import torch
from torch import nn
from torch.nn import functional as F


class LayerNorm(nn.LayerNorm):
    def __init__(self, *args, **kwargs):
        """Faster LayerNorm by seting elementwise_affine=False."""
        super().__init__(*args, **kwargs, elementwise_affine=False)


class RMSNorm(nn.Module):
    def __init__(self, dim: int):
        """RNMSNorm from https://arxiv.org/abs/1910.07467. Slower than LayerNorm."""
        super().__init__()
        self.scale = dim**0.5
        self.weight = nn.Parameter(torch.ones(dim))

    def _norm(self, x):
        return x * torch.rsqrt(x.pow(2).mean(-1, keepdim=True) + 1e-12)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # return F.normalize(x, dim=-1) * self.scale * self.weight
        return self._norm(x.float()).type_as(x) * self.weight

    def __repr__(self):
        return f"RMSNorm(dim={self.weight.shape[0]})"
