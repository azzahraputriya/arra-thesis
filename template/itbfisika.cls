% itbfisika.cls -- ITB Sarjana Fisika thesis (Buku TA) class.
%
% Port of the official "Template Buku TA versi 1.0" from https://fi.itb.ac.id
% (21 Feb 2022, edited by Laurenzius Yudha Prasetya Tama, FI 2017, based on
% Cica Gustiani's TF 2007 template).
% The look matches the original. Changes from it, and why:
%   - Built for XeTeX (tectonic), not pdfLaTeX. Text font is TeX Gyre Termes
%     (a Times clone) through fontspec, because the original T1 Times font
%     silently drops characters like en-dashes and curly quotes under XeTeX.
%     Math still uses mathptmx, as in the original.
%   - Fixed pages (cover, approval page, lists) are commands here, so the
%     thesis files only hold content. Identity is set with \judul{} etc.
%   - Bugs fixed: the 2-supervisor approval page printed supervisor 1 twice,
%     the inner cover had a hardcoded year, examiners were hardcoded, and the
%     abbreviations list was missing from the table of contents.
%   - A4 paper. The original passed `a4`, which is not a real option, so its
%     PDFs came out US Letter.
%   - No \nocite{*}: the reference list only shows works actually cited.
%   - Loads icomma, so decimal commas in math ($1,5$) print without a space.
\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{itbfisika}[2026/11/07 ITB Sarjana Fisika Buku TA]

\LoadClass[12pt,a4paper,fleqn]{extreport}

% --- Identity (set these in main.tex) ---------------------------------------
\newcommand\judul[1]{\gdef\@judul{#1}}
\newcommand\judulinggris[1]{\gdef\@judulinggris{#1}}
\newcommand\penulis[1]{\gdef\@penulis{#1}}
\newcommand\nim[1]{\gdef\@nim{#1}}
\newcommand\tahun[1]{\gdef\@tahun{#1}}
\newcommand\katakunci[1]{\gdef\@katakunci{#1}}
\newcommand\keywords[1]{\gdef\@keywords{#1}}
% \pembimbing{name}{NIP}; \pembimbingdua is optional and switches the
% approval page to the two-supervisor layout.
\newcommand\pembimbing[2]{\gdef\@pembimbingsatu{#1}\gdef\@nipsatu{#2}}
\newcommand\pembimbingdua[2]{\gdef\@pembimbingdua{#1}\gdef\@nipdua{#2}}
\newcommand\penguji[2]{\gdef\@pengujisatu{#1}\gdef\@pengujidua{#2}}

\judul{Judul Tugas Akhir}
\judulinggris{Thesis Title}
\penulis{Nama Mahasiswa}
\nim{102TTNNN}
\tahun{\the\year}
\katakunci{}
\keywords{}
\pembimbing{Nama Pembimbing}{NIP}
\penguji{Nama Penguji 1}{Nama Penguji 2}

% --- Page and fonts ----------------------------------------------------------
\RequirePackage{geometry}
\geometry{verbose,tmargin=3cm,bmargin=3cm,lmargin=4cm,rmargin=3cm}

\RequirePackage{mathptmx}
\RequirePackage[no-math]{fontspec}
\setmainfont{texgyretermes}[
  Extension = .otf,
  UprightFont = *-regular,
  BoldFont = *-bold,
  ItalicFont = *-italic,
  BoldItalicFont = *-bolditalic]

\RequirePackage[american,bahasa]{babel} % last listed = main language
\RequirePackage[bookmarks=true,unicode=true,pdfusetitle,bookmarksnumbered=true,
  bookmarksopen=true,breaklinks=true,pdfborder={0 0 1},backref=true,
  colorlinks=false]{hyperref}
\AtBeginDocument{\hypersetup{pdfauthor={\@penulis},pdfsubject={SKRIPSI},
  pdftitle={\@judul},pdfkeywords={\@keywords}}}

\RequirePackage[htt]{hyphenat}
\RequirePackage{listing}
\RequirePackage{listings}
\RequirePackage{graphicx}
\RequirePackage{tabularx}
\RequirePackage{float}
\RequirePackage[hang,nooneline,scriptsize,md]{subfigure}
\RequirePackage[font=small,labelfont=bf]{caption}
\RequirePackage[onehalfspacing]{setspace}
\RequirePackage{indentfirst}
\RequirePackage{parskip}
\RequirePackage[titletoc]{appendix}
\RequirePackage{cite}
\RequirePackage{amssymb}
\RequirePackage{amsmath}
% Indonesian decimal comma: $1,5$ prints as 1,5, not 1, 5. A comma followed
% by a space, as in $(a, b)$, keeps its space.
\RequirePackage{icomma}
\RequirePackage{mathrsfs}
\RequirePackage{dsfont}
\RequirePackage{relsize}

% The original \include'd every page, which ended the page before numbering
% changed. Without that, the last front page would get page number 1.
\let\itb@pagenumbering\pagenumbering
\renewcommand\pagenumbering[1]{\clearpage\itb@pagenumbering{#1}}

\pagestyle{plain}
\setlength{\parindent}{20pt}

\hyphenation{di-la-ku-kan be-ri-kut a-da-lah}

% --- Headings ----------------------------------------------------------------
\RequirePackage{titlesec}
\titleformat{\chapter}[display]
  {\bfseries\Large}
  {\filcenter\LARGE\MakeUppercase\chaptertitlename\ \LARGE\thechapter}
  {0mm}
  {\filcenter}
\titleformat*{\section}{\bfseries\large}
\titleformat*{\subsection}{\bfseries}
\titlespacing*{\chapter}{0pt}{-1.5\baselineskip}{1em}
\renewcommand{\thechapter}{\Roman{chapter}}

% --- Table of contents and lists ---------------------------------------------
\RequirePackage[subfigure]{tocloft}
\renewcommand{\cftpartleader}{\dotfill}
\renewcommand{\cftpartafterpnum}{\cftparfillskip}
\renewcommand{\cftchapleader}{\dotfill}
\renewcommand{\cftsecleader}{\dotfill}
\renewcommand{\cftsubsecleader}{\dotfill}

\renewcommand*\cftchappresnum{\MakeUppercase{bab}~}
\renewcommand\chaptername{BAB}
% Fits the widest number (BAB VIII); the original only fitted "BAB", so
% "BAB III" ran into its title.
\settowidth{\cftchapnumwidth}{\bfseries BAB~VIII}
\renewcommand{\cftchapaftersnumb}{\quad}
\addtocontents{toc}{%
  \protect\renewcommand*\protect\cftchappresnum{\MakeUppercase{\chaptername}~}}

\RequirePackage{chngcntr}
\renewcommand{\cftfigpresnum}{\bfseries Gambar\ }
\renewcommand{\cfttabpresnum}{\bfseries Tabel\ }
\newlength{\itb@len}
\settowidth{\itb@len}{\cftfigpresnum}
\setlength{\cftfignumwidth}{\dimexpr\itb@len+2em}
\settowidth{\itb@len}{\cfttabpresnum}
\setlength{\cfttabnumwidth}{\dimexpr\itb@len+2em}

% Bibliography without its own heading; \daftarpustaka prints one.
\renewenvironment{thebibliography}[1]{%
  \section*{\refname}%
  \@mkboth{\MakeUppercase\refname}{\MakeUppercase\refname}%
  \list{\@biblabel{\@arabic\c@enumiv}}%
       {\settowidth\labelwidth{\@biblabel{#1}}%
        \leftmargin\labelwidth
        \advance\leftmargin\labelsep
        \@openbib@code
        \usecounter{enumiv}%
        \let\p@enumiv\@empty
        \renewcommand\theenumiv{\@arabic\c@enumiv}}%
  \sloppy
  \clubpenalty4000
  \@clubpenalty \clubpenalty
  \widowpenalty4000%
  \sfcode`\.\@m}
 {\def\@noitemerr{\@latex@warning{Empty `thebibliography' environment}}%
  \endlist}

% Appendices: "LAMPIRAN A" headings, after \appendix.
\newcommand\appendix@chapter[1]{%
  \refstepcounter{chapter}%
  \orig@chapter*{LAMPIRAN \@Alph\c@chapter \\ #1}\vspace{1.5em}%
  \addcontentsline{toc}{chapter}{LAMPIRAN \@Alph\c@chapter: #1}%
}
\let\orig@chapter\chapter
\g@addto@macro\appendix{\let\chapter\appendix@chapter}

% --- Fixed pages -------------------------------------------------------------
% Starts an unnumbered front-matter page with a centred heading and a ToC line.
\newcommand\itb@halaman[1]{%
  \clearpage\phantomsection
  \addcontentsline{toc}{chapter}{#1}}

\newcommand\sampul{%
  \begin{titlepage}
  \begin{center}
  \begin{doublespace}
  \textbf{\smaller\Large{\MakeUppercase{\@judul}}}\\[3cm]
  \end{doublespace}
  \textbf{\MakeUppercase{\large tugas akhir}}\\
  \textbf{Karya tulis sebagai salah satu syarat\\ untuk memperoleh gelar
    Sarjana dari\\ Institut Teknologi Bandung}\\[2cm]
  \textbf{Oleh} \\
  \textbf{\MakeUppercase{\large{\@penulis}}} \\
  \textbf{\large NIM} \textbf{\large{\@nim}}\\[2cm]
  \includegraphics[width=0.18\linewidth]{logo-itb}
  \vfill
  \textbf{\large \MakeUppercase{program studi sarjana fisika}}\\
  \textbf{\MakeUppercase{fakultas matematika dan ilmu pengetahuan alam}}\\
  \textbf{\large \MakeUppercase{institut teknologi bandung}}\\
  \textbf{\large \@tahun}\\
  \end{center}
  \end{titlepage}}

\newcommand\sampuldalam{%
  \clearpage\thispagestyle{empty}
  \begin{center}
  \begin{doublespace}
  \textbf{\smaller\large{\MakeUppercase{\@judul}}}\\[2.5cm]
  \end{doublespace}
  \textbf{\MakeUppercase{\large tugas akhir}}\\[0.5cm]
  \begin{onehalfspace}
  Diajukan untuk memenuhi syarat kelulusan tahap pendidikan strata-1 pada\\
  Program Studi Fisika -- Institut Teknologi Bandung\\[1.8cm]
  \end{onehalfspace}
  \large Oleh: \\
  \begin{onehalfspace}
  \large{\@penulis} \\
  \large{\@nim}\\[1.5cm]
  \end{onehalfspace}
  \vspace{1.5cm}
  \large Pembimbing: \\
  \begin{onehalfspace}
  \large{\@pembimbingsatu}
  \ifdefined\@pembimbingdua \\ \large{\@pembimbingdua}\fi
  \end{onehalfspace}
  \vfill
  \textbf{\large \MakeUppercase{program studi fisika}}\\
  \textbf{\large \MakeUppercase{fakultas matematika dan ilmu pengetahuan alam}}\\
  \textbf{\large \MakeUppercase{institut teknologi bandung}}\\
  \textbf{\large \@tahun}\\
  \end{center}}

\newcommand\pengesahan{%
  \itb@halaman{LEMBAR PENGESAHAN}
  \begin{center}
  \begin{doublespace}
  \textbf{\Large \MakeUppercase{pengesahan}}
  \end{doublespace}
  \end{center}
  \begin{center}
  \begin{doublespace}
  \textbf{\Large\MakeUppercase{\@judul}}
  \end{doublespace}
  \end{center}
  \begin{center}
  Oleh\\
  \textbf{\@penulis}\\
  \textbf{NIM \@nim}\\[1.5cm]
  \textbf{Program studi Sarjana Fisika\\
  Fakultas Matematika dan Ilmu Pengetahuan Alam\\
  Institut Teknologi Bandung}\\[1cm]
  \vfill
  Menyetujui\\[1cm]
  \end{center}
  \ifdefined\@pembimbingdua
    \noindent Bandung, \today\\[1em]
    \begin{minipage}{0.35\textwidth}
    Dosen Pembimbing 1,\\[2cm]
    \@pembimbingsatu\\
    NIP. \@nipsatu
    \end{minipage}
    \hfill
    \begin{minipage}{0.35\textwidth}
    Dosen Pembimbing 2,\\[2cm]
    \@pembimbingdua\\
    NIP. \@nipdua
    \end{minipage}
  \else
    \begin{center}
    Bandung, \today\\
    Dosen Pembimbing, \\[2cm]
    \@pembimbingsatu\\
    NIP. \@nipsatu
    \end{center}
  \fi
  \vfill
  Tim Penguji:\\
  1. \@pengujisatu\\
  2. \@pengujidua}

\newcommand\pedoman{%
  \itb@halaman{PEDOMAN PENGGUNAAN BUKU TUGAS AKHIR}
  \begin{center}
  \textbf{\Large{PEDOMAN PENGGUNAAN\\BUKU TUGAS AKHIR}}
  \end{center}
  \vspace{1.5cm}
  \noindent Buku Tugas Akhir Sarjana ini tidak dipublikasikan, namun terdaftar
  dan tersedia di Perpustakaan Institut Teknologi Bandung. Buku ini dapat
  diakses umum, dengan ketentuan bahwa penulis memiliki hak cipta dengan
  mengikuti aturan HaKI yang berlaku di Institut Teknologi Bandung. Referensi
  kepustakaan diperkenankan dicatat, tetapi pengutipan atau peringkasan hanya
  dapat dilakukan seizin penulis, dan harus disertai dengan kebiasaan ilmiah
  untuk menyebutkan sumbernya.

  Memperbanyak atau menerbitkan sebagian atau seluruh buku Tugas Akhir harus
  atas izin Program Studi Sarjana Fisika, Fakultas Matematika dan Ilmu
  Pengetahuan Alam, Institut Teknologi Bandung.}

% \persembahan{text}: dedication, centred on its own page.
\newcommand\persembahan[1]{%
  \clearpage
  \vspace*{\fill}
  \begingroup\centering\textit{#1}\par\endgroup
  \vspace*{\fill}}

\newcommand\daftarisi{%
  \itb@halaman{DAFTAR ISI}
  \renewcommand{\cftdotsep}{\cftnodots}
  \setlength{\cftbeforetoctitleskip}{-0.5cm}
  \renewcommand{\cfttoctitlefont}{\hfill\Large\bfseries}
  \renewcommand{\cftaftertoctitle}{\hfill\hfill}
  \renewcommand\contentsname{DAFTAR ISI}
  \tableofcontents}

\newcommand\daftargambar{%
  \itb@halaman{DAFTAR GAMBAR}
  \setlength{\cftbeforeloftitleskip}{-0.5cm}
  \renewcommand{\cftloftitlefont}{\hfill\Large\bfseries}
  \renewcommand{\cftafterloftitle}{\hfill}
  \renewcommand{\cftfigleader}{\dotfill}
  \renewcommand\listfigurename{DAFTAR GAMBAR}
  \listoffigures}

\newcommand\daftartabel{%
  \itb@halaman{DAFTAR TABEL}
  \renewcommand{\cfttableader}{\dotfill}
  \begin{center}{\bfseries \Large DAFTAR TABEL}\end{center}
  \vspace{2em}
  \@starttoc{lot}}

% \daftarpustaka{bibfile}: reference list, APA-like, cited works only.
\newcommand\daftarpustaka[1]{%
  \itb@halaman{DAFTAR PUSTAKA}
  \renewcommand{\refname}{}
  \begin{center}\textbf{\large DAFTAR PUSTAKA}\\[1em]\end{center}
  \bibliographystyle{apalike}
  \bibliography{#1}}

% --- Content environments ----------------------------------------------------
\newenvironment{abstrak}{%
  \itb@halaman{ABSTRAK}
  \begin{center}
  \textbf{\large ABSTRAK}\\[0.5cm]
  \textbf{\large \MakeUppercase{\@judul}}\\[0.5cm]
  \textbf{Oleh}\\
  \textbf{\@penulis}\\
  \textbf{NIM: \@nim}\\[2em]
  \end{center}
  \noindent\ignorespaces}
 {\par\noindent Kata kunci: \@katakunci}

% English abstract: hyphenates as English.
\renewenvironment{abstract}{%
  \itb@halaman{ABSTRACT}
  \begin{otherlanguage}{american}
  \begin{center}
  \textbf{\large ABSTRACT}\\[0.5cm]
  \textbf{\large \MakeUppercase{\@judulinggris}}\\[0.5cm]
  \textbf{by}\\
  \textbf{\@penulis}\\
  \textbf{NIM: \@nim}\\[2em]
  \end{center}
  \noindent\ignorespaces}
 {\par\noindent Key words: \@keywords
  \end{otherlanguage}}

% Foreword; the author's name and NIM are signed at the end.
\newenvironment{katapengantar}{%
  \itb@halaman{KATA PENGANTAR}
  \begin{center}\textbf{\large KATA PENGANTAR}\\[3em]\end{center}}
 {\begin{flushright}
  Bandung, \today\\[0.25cm]
  \@penulis\\
  \@nim
  \end{flushright}}

% Symbol / abbreviation lists. Rows are `symbol & meaning \\`.
\newcommand\itb@daftar[2]{%
  \itb@halaman{#1}
  \begin{center}{\bfseries \Large #1}\end{center}
  \vspace{3em}
  \begin{center}
  % Plain tabular, not tabularx: tabularx reads its body ahead and would lose
  % the closing \hline that lives in the end code.
  \begin{tabular}{>{\raggedright\arraybackslash}p{\dimexpr0.4\textwidth-2\tabcolsep}
                  >{\raggedright\arraybackslash}p{\dimexpr0.4\textwidth-2\tabcolsep}}
  \hline
  \textbf{#2} & \textbf{Arti} \\
  \hline}
\newcommand\itb@akhirdaftar{\hline\end{tabular}\end{center}}
\newenvironment{daftarnotasi}{\itb@daftar{DAFTAR NOTASI}{Notasi}}{\itb@akhirdaftar}
\newenvironment{daftarsingkatan}{\itb@daftar{DAFTAR SINGKATAN}{Singkatan}}{\itb@akhirdaftar}
