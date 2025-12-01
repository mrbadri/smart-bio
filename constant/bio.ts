export interface BiologyTextbook {
  chapters: {
    id: number;
    title: string;
    page: number;
    range: { from: number; to: number };
    lectures: {
      id: number;
      title: string;
      page: number;
    }[];
  }[];
}

export const BIOLOGY_TEXTBOOK: BiologyTextbook = {
  chapters: [
    {
      id: 1,
      title: "دنیای زنده",
      page: 1,
      range: { from: 1, to: 16 },
      lectures: [
        { id: 1, title: "زیست‌شناسی چیست؟", page: 2 },
        { id: 2, title: "گسترهٔ حیات", page: 7 },
        { id: 3, title: "بدن انسان در بافت و یاخته", page: 11 },
      ],
    },
    {
      id: 2,
      title: "گوارش و جذب مواد",
      page: 17,
      range: { from: 17, to: 32 },
      lectures: [
        { id: 1, title: "ساختار و عملکرد لولهٔ گوارش", page: 18 },
        { id: 2, title: "جذب مواد و تنظیم فعالیت دستگاه گوارش", page: 25 },
        { id: 3, title: "تنوع گوارش در جانداران", page: 30 },
      ],
    },
    {
      id: 3,
      title: "تبادلات گازی",
      page: 33,
      range: { from: 33, to: 46 },
      lectures: [
        { id: 1, title: "کار و ساز دستگاه تنفس در انسان", page: 34 },
        { id: 2, title: "تهویۀ ششی", page: 40 },
        { id: 3, title: "تنوع تبادلات گازی", page: 45 },
      ],
    },
    {
      id: 4,
      title: "گردش مواد در بدن",
      page: 47,
      range: { from: 47, to: 68 },
      lectures: [
        { id: 1, title: "قلب", page: 48 },
        { id: 2, title: "رگ‌ها", page: 55 },
        { id: 3, title: "خون", page: 61 },
        { id: 4, title: "تنوع گردش مواد در جانداران", page: 65 },
      ],
    },
    {
      id: 5,
      title: "تنظیم اسمزی و دفع مواد زائد",
      page: 69,
      range: { from: 69, to: 78 },
      lectures: [
        { id: 1, title: "کلیه‌ها و هم‌ایستایی", page: 70 },
        { id: 2, title: "تشکیل ادرار و تخلیۀ آن", page: 73 },
        { id: 3, title: "تنوع تنظیم اسمزی و دفع در جانداران", page: 76 },
      ],
    },
    {
      id: 6,
      title: "از یاخته تا گیاه",
      page: 79,
      range: { from: 79, to: 96 },
      lectures: [
        { id: 1, title: "ویژگی‌های یاخته‌های گیاهی", page: 80 },
        { id: 2, title: "سامانۀ بافتی", page: 86 },
        { id: 3, title: "ساختار گیاهان", page: 90 },
      ],
    },
    {
      id: 7,
      title: "جذب و انتقال مواد در گیاهان",
      page: 97,
      range: { from: 97, to: 105 }, // تا آخرین گفتارِ موجود در لیست
      lectures: [
        { id: 1, title: "تغذیۀ گیاهی", page: 98 },
        { id: 2, title: "جانداران مؤثر در تغذیۀ گیاهی", page: 102 },
        { id: 3, title: "انتقال مواد در گیاهان", page: 105 },
      ],
    },
  ],
};
