from fastapi import APIRouter, HTTPException

from backend.schemas.document import (
    DocumentRequest,
    DocumentResponse,
)
from backend.services.document_service import DISCLAIMER
from backend.services.gemini_service import GeminiService


router = APIRouter()


@router.post(
    "/generate",
    response_model=DocumentResponse,
)
async def generate_document(
    request: DocumentRequest,
):

    try:

        service = GeminiService()

        content = service.generate_document(
            document_type=request.document_type,
            user_prompt=request.user_prompt,
            jurisdiction=request.jurisdiction or "India",
            party_one=request.party_one or "",
            party_two=request.party_two or "",
            additional_details=request.additional_details or "",
        )

        return DocumentResponse(
            success=True,
            document_type=request.document_type,
            content=content,
            disclaimer=DISCLAIMER,
        )

    except ValueError as exc:

        raise HTTPException(
            status_code=500,
            detail=str(exc),
        ) from exc

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=(
                "Unable to generate the document. "
                f"Details: {str(exc)}"
            ),
        )