import { BIOLOGY_TEXTBOOK } from "@/constant/bio";
import { getChapterAndLectureByPage } from "./get-chapter";
import { PageTextResult } from "pdf-parse";

export interface PageParsed {
  content: string;
  page: number;
  chapter: string | null;
  lecture: string | null;
}

export const pageParser = (pages: PageTextResult[]): PageParsed[] => {
  return pages.map(({ num, text }) => {
    const result = getChapterAndLectureByPage(num, BIOLOGY_TEXTBOOK);

    return {
      content: text,
      page: num,
      chapter: result?.chapter?.title ?? null,
      lecture: result?.lecture?.title ?? null,
    };
  });
};
