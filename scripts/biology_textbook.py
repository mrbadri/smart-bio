"""
Biology Textbook Structure - Persian Biology Book (Grade 10)

Contains the table of contents with chapters, lectures, and page ranges.
"""

from dataclasses import dataclass
from typing import List, Optional, Dict


@dataclass
class Lecture:
    """Represents a lecture (گفتار) within a chapter"""
    id: int
    title: str
    page: int


@dataclass
class Chapter:
    """Represents a chapter (فصل) in the textbook"""
    id: int
    title: str
    page: int
    range: Dict[str, int]  # {"from": int, "to": int}
    lectures: List[Lecture]


@dataclass
class BiologyTextbook:
    """Complete textbook structure"""
    chapters: List[Chapter]


# Biology Textbook Data (Grade 10)
BIOLOGY_TEXTBOOK = BiologyTextbook(
    chapters=[
        Chapter(
            id=1,
            title="دنیای زنده",
            page=1,
            range={"from": 1, "to": 16},
            lectures=[
                Lecture(id=1, title="زیست‌شناسی چیست؟", page=2),
                Lecture(id=2, title="گسترهٔ حیات", page=7),
                Lecture(id=3, title="بدن انسان در بافت و یاخته", page=11),
            ],
        ),
        Chapter(
            id=2,
            title="گوارش و جذب مواد",
            page=17,
            range={"from": 17, "to": 32},
            lectures=[
                Lecture(id=1, title="ساختار و عملکرد لولهٔ گوارش", page=18),
                Lecture(id=2, title="جذب مواد و تنظیم فعالیت دستگاه گوارش", page=25),
                Lecture(id=3, title="تنوع گوارش در جانداران", page=30),
            ],
        ),
        Chapter(
            id=3,
            title="تبادلات گازی",
            page=33,
            range={"from": 33, "to": 46},
            lectures=[
                Lecture(id=1, title="کار و ساز دستگاه تنفس در انسان", page=34),
                Lecture(id=2, title="تهویۀ ششی", page=40),
                Lecture(id=3, title="تنوع تبادلات گازی", page=45),
            ],
        ),
        Chapter(
            id=4,
            title="گردش مواد در بدن",
            page=47,
            range={"from": 47, "to": 68},
            lectures=[
                Lecture(id=1, title="قلب", page=48),
                Lecture(id=2, title="رگ‌ها", page=55),
                Lecture(id=3, title="خون", page=61),
                Lecture(id=4, title="تنوع گردش مواد در جانداران", page=65),
            ],
        ),
        Chapter(
            id=5,
            title="تنظیم اسمزی و دفع مواد زائد",
            page=69,
            range={"from": 69, "to": 78},
            lectures=[
                Lecture(id=1, title="کلیه‌ها و هم‌ایستایی", page=70),
                Lecture(id=2, title="تشکیل ادرار و تخلیۀ آن", page=73),
                Lecture(id=3, title="تنوع تنظیم اسمزی و دفع در جانداران", page=76),
            ],
        ),
        Chapter(
            id=6,
            title="از یاخته تا گیاه",
            page=79,
            range={"from": 79, "to": 96},
            lectures=[
                Lecture(id=1, title="ویژگی‌های یاخته‌های گیاهی", page=80),
                Lecture(id=2, title="سامانۀ بافتی", page=86),
                Lecture(id=3, title="ساختار گیاهان", page=90),
            ],
        ),
        Chapter(
            id=7,
            title="جذب و انتقال مواد در گیاهان",
            page=97,
            range={"from": 97, "to": 105},
            lectures=[
                Lecture(id=1, title="تغذیۀ گیاهی", page=98),
                Lecture(id=2, title="جانداران مؤثر در تغذیۀ گیاهی", page=102),
                Lecture(id=3, title="انتقال مواد در گیاهان", page=105),
            ],
        ),
    ]
)


def get_chapter_and_lecture_by_page(
    page: int, 
    textbook: BiologyTextbook = BIOLOGY_TEXTBOOK
) -> Optional[Dict]:
    """
    Find chapter and lecture information for a given page number
    
    Args:
        page: Page number to look up
        textbook: BiologyTextbook instance (defaults to BIOLOGY_TEXTBOOK)
        
    Returns:
        Dictionary with chapter and lecture info, or None if not found
        
    Example:
        >>> result = get_chapter_and_lecture_by_page(18)
        >>> print(result['chapter']['title'])
        'گوارش و جذب مواد'
        >>> print(result['lecture']['title'])
        'ساختار و عملکرد لولهٔ گوارش'
    """
    if not isinstance(page, int) or page < 1:
        return None
    
    # Find the chapter
    chapter = None
    for ch in textbook.chapters:
        if ch.range["from"] <= page <= ch.range["to"]:
            chapter = ch
            break
    
    if not chapter:
        return None
    
    # Find the lecture within the chapter
    lecture = None
    lectures = chapter.lectures
    
    for i, lec in enumerate(lectures):
        start = lec.page
        # End is either the start of next lecture - 1, or end of chapter
        end = lectures[i + 1].page - 1 if i < len(lectures) - 1 else chapter.range["to"]
        
        if start <= page <= end:
            lecture = {
                "id": lec.id,
                "title": lec.title,
                "page": lec.page,
                "range": {"from": start, "to": end}
            }
            break
    
    return {
        "chapter": {
            "id": chapter.id,
            "title": chapter.title,
            "page": chapter.page,
            "range": chapter.range
        },
        "lecture": lecture
    }


def get_chapter_info(page: int, textbook: BiologyTextbook = BIOLOGY_TEXTBOOK) -> Optional[Dict]:
    """
    Get only chapter information for a page (without lecture details)
    
    Args:
        page: Page number
        textbook: BiologyTextbook instance
        
    Returns:
        Dictionary with chapter info or None
    """
    result = get_chapter_and_lecture_by_page(page, textbook)
    return result["chapter"] if result else None


def get_lecture_info(page: int, textbook: BiologyTextbook = BIOLOGY_TEXTBOOK) -> Optional[Dict]:
    """
    Get only lecture information for a page
    
    Args:
        page: Page number
        textbook: BiologyTextbook instance
        
    Returns:
        Dictionary with lecture info or None
    """
    result = get_chapter_and_lecture_by_page(page, textbook)
    return result["lecture"] if result and result["lecture"] else None

