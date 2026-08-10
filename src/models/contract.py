from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True, frozen=True)
class Contract:

    numero: str
    prefixo_unidade: str
    objeto: str
    data_atualizacao: datetime

    @classmethod
    def from_api(
        cls,
        data: dict,
    ) -> "Contract":

        objeto = data.get(
            "objetoContrato",
            "",
        )

        print("OBJETO RECEBIDO:")
        print(objeto)

        prefixo = (
            objeto.split("/")[0]
            .strip()
        )

        print("PREFIXO EXTRAÍDO:")
        print(prefixo)

        return cls(
            numero=data.get(
                "numeroControlePNCP",
                "",
            ),
            prefixo_unidade=prefixo,
            objeto=objeto,
            data_atualizacao=datetime.fromisoformat(
                data["dataAtualizacao"].replace(
                    "Z",
                    "+00:00",
                )
            ),
        )

    @property
    def data_formatada(self) -> str:

        return self.data_atualizacao.strftime(
            "%d/%m/%Y"
        )