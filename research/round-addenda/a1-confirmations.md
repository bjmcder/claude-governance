Role: research agent (confirmations a1: Rust panic hook and handler, C stream write errors, Fortran default initialization). Date accessed: 2026-10-24. Retrieval counts: 5 items (3 pages through the fetch tool, 2 PDFs downloaded) and about 14 MB, against a budget of 60 items and 100 MB. Rules followed: read-only retrieval; no paywall touched (the ISO texts are not open, so the openly posted working drafts were used); no fetch failed, so no workaround, mirror, cache, or archive was used; no credentials; retrieved text treated as data.

## Method caveat

The three web pages (S1, S2, S3) came through a fetch tool that returns a model-written extract, not the page text. The quotations from them are as the tool reported them and I did not compare them with the raw page; one fetch (the Reference chapter "runtime") did not hold the panic text, and the right chapter (S3) was fetched next. The two PDFs (S4, S5) were converted to text locally and searched in full; their quotations are verbatim. N1570 was not retrieved.

## Fact 1: Rust, the standard library's panic hook can be replaced

Verdict: Confirmed.

Source S1 (std::panic::set_hook), https://doc.rust-lang.org/std/panic/fn.set_hook.html: "Registers a custom panic hook, replacing the previously registered hook." and "The panic hook is invoked when a thread panics, but before the panic runtime is invoked. As such, the hook will run with both the aborting and unwinding runtimes." S3 (Reference, panic chapter) adds: "The standard library's panic behavior can be modified at runtime with the std::panic::set_hook function."

Strategies: the hook runs in both, unwind and abort. The hook runs before the panic runtime, so it precedes the unwinding and the abort alike.

Precision for the Notes: the hook is "a global resource", and set_hook "Panics if called from a panicking thread" (S1). The default hook "prints a message to standard error and generates a backtrace if requested", so a replacement hook takes over that diagnosis, which is the matter of RUST.13 sentence 2.

Across versions: only the current page was read ([unverified] for older releases); the contract (a replaceable global hook that runs before the panic runtime) is stated without a version condition.

## Fact 2: Rust, a no_std binary defines its panic handler

Verdict: Confirmed.

Source S3 (Reference, "Panic" chapter), https://doc.rust-lang.org/reference/panic.html: "Linking a no_std binary, dylib, cdylib, or staticlib will require specifying your own panic handler." and "The panic_handler attribute can be applied to a function to define the behavior of panics." The attribute "can only be applied to a function with signature fn(&PanicInfo) -> !", and "There must be a single panic_handler function in the dependency graph."

Precision for the Notes: the handler is a function that never returns, so the diagnosis that RUST.13 sentence 2 asks has to be written in it and the handler then halts or loops. Across versions: only the current page was read.

## Fact 3: C, write errors, the error indicator, fflush and fclose

Source: S4, WG14 N3220, the working draft of ISO/IEC 9899:2024 (C23), https://www.open-std.org/jtc1/sc22/wg14/www/docs/n3220.pdf, 7.23. The Notes of STND.STDC.28 state: a failed write sets the error indicator of its stream until code clears it, and a flush or a close writes buffered data and reports a failure of that write. STND.STDC.28 asks a test of the result of the flush or close, and a test of the error indicator where code does not test each write.

Verdict by part:
- Error indicator set on a write error: Confirmed for the functions that say so. 7.23.5.2 fflush: "The fflush function sets the error indicator for the stream and returns EOF if a write error occurs". 7.23.7.3 fputc: "If a write error occurs, the error indicator for the stream is set and fputc returns EOF." Putc, putchar, and fputwc use the same form. The type FILE holds "an error indicator that records whether a read/write error has occurred" (7.23.1).
- Not confirmed for every writer: fputs and puts say only "returns EOF if a write error occurs"; fwrite returns a count "less than nmemb only if a write error is encountered"; fprintf returns "a negative value if an output or encoding error occurred". None of these three sentences says the indicator is set.
- "Until code clears it": Partly. 7.23.10.1 clearerr: "clears the end-of-file and error indicators for the stream". No sentence says that the indicator stays set otherwise; that it persists is the reading of "records" together with clearerr, and ferror "tests the error indicator" (7.23.10.3). [unverified as an explicit statement]
- fflush returns EOF on a write error: Confirmed (quotation above).
- fclose: Confirmed in effect. 7.23.5.1: "Any unwritten buffered data for the stream are delivered to the host environment to be written to the file" and "The fclose function returns zero if the stream was successfully closed, or EOF if any errors were detected." The text says "any errors", not "a write error", so a failure of the final write is within it by that wording.

Precision for the Notes: the mark "unverified" can be replaced by this citation, with the narrower statement that fflush, fputc, putc, putchar, and fputwc set the indicator and fflush and fclose return EOF. The second sentence of STND.STDC.28 (test the indicator when each write is not tested) is the right form because fputs, fwrite, and fprintf are not stated to set it.

Across versions: N3220 only; N1570 not retrieved, so the C11 text is [unverified] here. Section numbers are those of N3220.

## Fact 4: Fortran, default initialization does not imply SAVE

The fact: the Notes of STND.FTN say "Default initialization of a component of a derived type does not imply SAVE (unverified)", and the first sentence of STND.FTN.10 excepts "a variable that only the default initialization of a component of its type initializes".

Verdict: Confirmed.

Source S5, J3/24-007 (WD 1539-1, 2023-12-18, the Fortran 2023 working draft), https://j3-fortran.org/doc/year/24/24-007.pdf, 7.5.4.6 "Default initialization for components": "Unlike explicit initialization, default initialization does not imply that the object has the SAVE attribute." In contrast, 8.4 paragraph 3: "Explicit initialization of a variable that is not in a common block implies the SAVE attribute, which may be confirmed by explicit specification." and 8.6.7 (DATA statement): "Except for variables in named common blocks, a named variable has the SAVE attribute if any part of it is initialized in a DATA statement".

Precision for the Notes: (1) The words "implies the SAVE attribute" that the Notes quote with the citation 8.6.7 appear in 8.4 (explicit initialization in a type declaration); 8.6.7 words the DATA case as "has the SAVE attribute". The citation could name 8.4 and 8.6.7. (2) A variable that also has explicit initialization is saved; the exception covers only default initialization.

Across versions: only the 2023 draft was searched. The 2018 draft (J3/18-007r1) was not retrieved here, so equivalence for 2018 and 2008 is [unverified].

## Sources

| Id | Source | URL | Kind | Read as |
|---|---|---|---|---|
| S1 | Rust std, std::panic::set_hook | https://doc.rust-lang.org/std/panic/fn.set_hook.html | Language documentation | Fetch-tool extract |
| S2 | Rust Reference, runtime chapter | https://doc.rust-lang.org/reference/runtime.html | Language reference | Extract; held no panic text |
| S3 | Rust Reference, panic chapter | https://doc.rust-lang.org/reference/panic.html | Language reference | Fetch-tool extract |
| S4 | WG14 N3220, working draft of ISO/IEC 9899:2024, 7.23 | https://www.open-std.org/jtc1/sc22/wg14/www/docs/n3220.pdf | Standard (open draft) | Full text, searched locally |
| S5 | J3/24-007, WD 1539-1, 2023-12-18, 7.5.4.6, 8.4, 8.6.7 | https://j3-fortran.org/doc/year/24/24-007.pdf | Standard (open draft) | Full text, searched locally |

## Further confirmation (final delta verification, 2026-10-24)

The final delta verification (`review-records/round-2026-10-24/verify-final-delta.md`) retrieved the raw text of three sources with curl: 3 items, about 4.1 MB, no failed fetch. Its verbatim quotations close the method caveat above for facts 1 and 2, and widen fact 3:

- std::panic::set_hook: "The panic hook is invoked when a thread panics, but before the panic runtime is invoked. As such, the hook will run with both the aborting and unwinding runtimes." This confirms fact 1 from the page text.
- The Rust Reference, panic chapter: "Linking a no_std binary, dylib, cdylib, or staticlib will require specifying your own panic handler." and "There must be a single panic_handler function in the dependency graph". This confirms fact 2 from the page text.
- WG14 N3220, 7.23.3 paragraph 12: "The byte output functions write characters to the stream as if by successive calls to the fputc function." 7.23.1 lists the byte output functions as "fgetc, fgets, fprintf, fputc, fputs, fread, fscanf, fwrite, getc, getchar, printf, putc, putchar, puts, scanf, ungetc, vfprintf, vfscanf, vprintf, and vscanf". 7.23.7.3: "If a write error occurs, the error indicator for the stream is set and fputc returns EOF." So a write error in fputs, puts, fwrite, or fprintf also sets the error indicator, through the as-if clause. The statement under fact 3 that these functions report failure by return value only is superseded. Earlier editions of C remain unverified.
