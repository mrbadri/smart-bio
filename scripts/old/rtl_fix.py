import re

# کاراکترهای عربی/فارسی
ARABIC_CHARS = re.compile(r'[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF]')
# تشخیص بخش‌های LTR مثل لینک، ایمیل، کلمات انگلیسی/عدد
LTR_SPAN = re.compile(
    r'(https?://\S+|[\w.+-]+@[\w-]+\.[\w.-]+|[A-Za-z0-9][A-Za-z0-9._:/\-]*)'
)

def is_rtl_line(line: str) -> bool:
    rtl = len(ARABIC_CHARS.findall(line))
    ltr = len(re.findall(r'[A-Za-z]', line))
    return rtl > ltr * 2  # heuristic

def fix_rtl_line(line: str) -> str:
    ltr_parts = []
    def repl(m):
        ltr_parts.append(m.group(0))
        return f"@@LTR{len(ltr_parts)-1}@@"

    temp = LTR_SPAN.sub(repl, line)
    tokens = temp.split()
    tokens.reverse()
    temp2 = " ".join(tokens)

    for i, part in enumerate(ltr_parts):
        temp2 = temp2.replace(f"@@LTR{i}@@", part)
    return temp2

def fix_rtl_text(text: str) -> str:
    out_lines = []
    for ln in text.splitlines():
        # هدرهای markdown، لیست‌ها، کد بلاک… را دست نزن
        if ln.strip().startswith(("#", "```", "-", "*", ">")) or not ln.strip():
            out_lines.append(ln)
            continue

        if is_rtl_line(ln):
            out_lines.append(fix_rtl_line(ln))
        else:
            out_lines.append(ln)
    return "\n".join(out_lines)