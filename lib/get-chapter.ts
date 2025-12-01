import { BiologyTextbook } from "@/constant/bio";

export function getChapterAndLectureByPage(
  page: number,
  tocObj: BiologyTextbook
) {
  if (typeof page !== "number" || page < 1) return null;

  const chapter =
    tocObj.chapters.find(
      (ch) => page >= ch.range.from && page <= ch.range.to
    ) || null;

  if (!chapter) return null;

  // پیدا کردن گفتار بر اساس رنج بین شروع گفتارها
  const lectures = chapter.lectures || [];
  let lecture = null;

  for (let i = 0; i < lectures.length; i++) {
    const start = lectures[i].page;
    const end =
      i < lectures.length - 1 ? lectures[i + 1].page - 1 : chapter.range.to;

    if (page >= start && page <= end) {
      lecture = { ...lectures[i], range: { from: start, to: end } };
      break;
    }
  }

  return { chapter, lecture };
}
