// template.typ — style sách kỹ thuật (technical book) cho Typst
//
// Dùng:
//   #import "template.typ": book
//   #show: book.with(title: "...", author: "...", subtitle: "...")
//   = Chapter 1
//   ...

#let accent = rgb("#2b6cb0")
#let code-bg = rgb("#f5f5f7")
#let code-border = rgb("#dcdce0")

#let book(
  title: "Untitled",
  subtitle: none,
  author: none,
  date: none,
  body,
) = {
  // ---- Font & page cơ bản ----
  set text(
    font: ("Libertinus Serif", "New Computer Modern"),
    size: 11pt,
    lang: "vi",
  )
  set page(
    paper: "a4",
    margin: (top: 3cm, bottom: 2.8cm, left: 2.8cm, right: 2.8cm),
    numbering: "1",
    header: context {
      if counter(page).get().first() > 1 [
        #set text(size: 9pt, fill: gray)
        #title
        #h(1fr)
        #context {
          let headings = query(selector(heading.where(level: 1)).before(here()))
          if headings.len() > 0 [ #headings.last().body ]
        }
        #line(length: 100%, stroke: 0.5pt + gray)
      ]
    },
  )
  set par(justify: true, leading: 0.65em, first-line-indent: 0em)

  // ---- Heading style ----
  set heading(numbering: "1.1")
  show heading.where(level: 1): it => {
    pagebreak(weak: true)
    v(1.5cm)
    text(size: 9pt, fill: accent, tracking: 2pt)[CHƯƠNG #counter(heading).display()]
    v(0.3cm)
    text(size: 24pt, weight: "bold")[#it.body]
    v(1cm)
  }
  show heading.where(level: 2): it => {
    v(0.8em)
    text(size: 15pt, weight: "bold", fill: accent)[#it.body]
    v(0.4em)
  }
  show heading.where(level: 3): it => {
    text(size: 12pt, weight: "bold")[#it.body]
    v(0.3em)
  }

  // ---- Code block style (raw block, ví dụ ```bash ... ```) ----
  show raw.where(block: true): it => {
    set text(font: ("DejaVu Sans Mono", "Liberation Mono"), size: 9.5pt)
    block(
      fill: code-bg,
      stroke: 1pt + code-border,
      radius: 4pt,
      inset: 10pt,
      width: 100%,
      it,
    )
  }
  // ---- Inline code style ----
  show raw.where(block: false): it => {
    set text(font: ("DejaVu Sans Mono", "Liberation Mono"), size: 0.95em)
    box(fill: code-bg, outset: (y: 2pt, x: 2pt), radius: 2pt, it)
  }

  // ---- Quote style ----
  show quote.where(block: true): it => {
    block(
      inset: (left: 1.2em, top: 0.5em, bottom: 0.5em),
      stroke: (left: 2.5pt + accent),
      it.body,
    )
  }

  // ---- Link style ----
  show link: it => text(fill: accent, it)

  // ================= Title page =================
  set page(numbering: none)
  align(center + horizon)[
    #v(-3cm)
    #line(length: 40%, stroke: 1.5pt + accent)
    #v(0.6cm)
    #text(size: 28pt, weight: "bold")[#title]
    #if subtitle != none [
      #v(0.4cm)
      #text(size: 15pt, fill: gray)[#subtitle]
    ]
    #v(0.6cm)
    #line(length: 40%, stroke: 1.5pt + accent)
    #v(2cm)
    #if author != none [#text(size: 12pt)[#author]]
    #if date != none [
      #v(0.3cm)
      #text(size: 10pt, fill: gray)[#date]
    ]
  ]
  pagebreak()

  // ================= Mục lục (TOC) =================
  outline(title: "Mục lục", indent: auto)
  pagebreak()

  // ================= Nội dung =================
  set page(numbering: "1")
  counter(page).update(1)
  body
}
