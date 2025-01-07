Title: Size Optimization Tricks

URL Source: https://justine.lol/sizetricks/

Markdown Content:
June 10th, 2022 @ justine's web page

Size Optimization Tricks

This blog post will cover some of the tricks I've used in the past to make c / c++ / python binaries smaller using x86 assembly. Much of it will revolve around the Cosmopolitan codebase, since I recently received feedback from the ELKS project that they love the code and want to hear more about how the tricks cosmo uses can potentially improve projects as intriguing as a i8086 Linux port. In many ways I feel a kinship with the ELKS project, since the first thing I had to do, to build Cosmopolitan, was write an i8086 bootloader called Actually Portable Executable. Plus it pleased me to hear that people who've been focusing on the problem a lot longer than I have are pleased with what they've read in Cosmopolitan so far. So I figured it'd be nice to share with a broader audience.

Table of Contents
Why It Matters
Look at the Binary
Field Arrangement
Run Length Encoding
Decentralized Sections
Dead Code Elimination
δzd Encoding
Overlapping Functions
Optimizing Printf
Tiny Portable ELF
Funding
See Also
Why It Matters
I like the UNIX philosphy of having lots of small programs. I like it so much, that the Cosmopolitan repository builds hundreds of them.
$ git clone https://github.com/jart/cosmopolitan
$ cd cosmopolitan
$ make -j16 MODE=tiny
$ find o/tiny -name \*.com | wc -l
741


The whole repository takes about fifty seconds to build from scratch on my PC. Out of those 741 executables, 403 are test executables. It's nice to have each set of tests be in a separate executable, to reduce the chance of a bad test messing up the global state, and leading to hard to diagnose unrelated failures somewhere else. It also means htop can serve as a test status free dashboard. Each dot com file is a static binary which behaves sort of like a Docker container, since they're usually zip files too which vendor assets (e.g. tzinfo data). Did I mention each executable also runs on seven operating systems?

# testing process
for f in $(find o/tiny/test -name \*_test.com); do
  for os in freebsd openbsd netbsd rhel7 rhel5 win7 win10 xnu; do
    scp $f $os:
    ssh $os ./${f##*/}
  done
done


So all I have to do to test all 400 programs on all 8 supported systems (3,200 tests total!) is simply scp them onto each host and run them. That takes about 15 seconds thanks to runit and runitd. It's been a big productivity boost and enables test-driven development (also known as TDD) with rapid feedback.

What makes this workflow manageable in that binaries are small. The tinier something is, the more instances we can have of it at scale. So it really isn't just about running on old computers. It's not necessarily about code golfing. It's about having infinitely more of a good thing on the cheap with a pleasant coding lifestyle. Here's some concrete examples of how small actually portable executables built with Cosmopolitan Libc can be:

 16K o/tiny/examples/hello2.com             # calls write  (links syscall)
 20K o/tiny/examples/hello.com              # calls fputs  (links stdio)
 24K o/tiny/examples/hello3.com             # calls printf (links fmt+stdio)
100K o/tiny/test/libc/calls/access_test.com # links test library
216K o/tiny/tool/net/redbean-original.com   # http/1.1 server
1.8M o/tiny/examples/pyapp/pyapp.com        # statically linked python app


Would my isolated hermetic testing workflow have been possible if I was using a language that needs at minimum 3mb to build a binary? My LAN only has gigabit ethernet. I don't need to work at a big company with industrial fabric switches to transfer these ~100kb test binaries over the wire. Let's do some back of the envelope calculations:

# theoretic minimum seconds transferring cosmo test binaries w/ 1gbps lan uncompressed
>>: (400*8 * 16*1000) / (1024*1024*1024/8)
0.3814697265625

# theoretic minimum seconds transferring go test binaries w/ 1gbps lan uncompressed
>>: (400*8 * 3*1000*1000) / (1024*1024*1024/8)
71.52557373046875 


That's a lot of time to be spending transfering files. Tiny isn't just about scale, but surviving long enough to scale. Cosmopolitan is a scrappy operation. The repo right now only has about 1.5 million lines of code. What I'm thinking about is how we're going to host the next billion lines of code, while everyone else is drowning in technical debt. Tiny is about the efficient use of resources. Big things must have small beginnings, because no one wants to build an empire of code on a tooling foundation that ravages their budget with cloud provider fees. Altavista ran an entire search engine on a single computer, and now you're telling me we need to plug our Full Story Elecron IDEs into a Kubernetes cluster to compile a C++ app that does math. How does that add up?

Losers always whine about how their bloat is a calculated tradeoff. The important thing to consider is that there is no tradeoff. Just engineers who've been victimized by the accidental complexity of modern software, chose to stop caring, and yearn for another break while their code compiles—like Dennis from Jurassic Park. Bloat is like the fake jobs version of scalability, in the sense that bloat offers hungry devs the thrill of complexity without the advantages. I used to operate a storage system with exabytes of data, and it honestly didn't feel that different from what I'm doing now, working on the tiniest software in the world. It's the stuff in the middle I just don't find as appealing.

In any case, as an avid reader of codebases, bloat is unpleasant. I think codebases have been lacking in a woman's touch for decades; and that especially applies to open source, which has never really had a woman's touch at all. We can fix that, but overall, the best way to improve software development is to make it more fun. There's few things more fun than size coding.

Look at the Binary

I think the biggest disadvantage of anyone looking to size optimize systemically is the difficulty of intuitive thinking. Especially for guys who use traditional hex editors. Here's what run-length encoded data looks like:

0002d0b0  01 00 01 03 01 06 01 09  01 0c 01 0f 01 12 14 1e  |................|
0002d0c0  01 15 04 1e 01 18 17 1e  01 1e 1c 1e 01 1b 00 00  |................|
0002d0d0  21 01 01 00 02 01 01 00  01 01 09 00 01 01 0a 00  |!...............|
0002d0e0  01 01 01 00 01 01 01 00  03 01 1a 00 04 01 01 00  |................|
0002d0f0  01 01 1a 00 03 01 01 00  81 01 00 00 00 00 00 00  |................|
0002d100  21 01 01 00 02 01 01 00  01 01 16 00 01 01 01 00  |!...............|
0002d110  01 01 1c 00 04 01 01 00  01 01 1a 00 03 01 01 00  |................|
0002d120  81 01 00 00 00 00 00 00  21 01 01 00 02 01 01 00  |........!.......|
0002d130  01 01 09 00 01 01 0c 00  01 01 01 00 03 01 1a 00  |................|


Hex editors are a really good tool when you're looking for a specific thing and need a specific answer, but they reveal little visually about the shape and form of a binary. You're not actually looking. You're just studying empirical data with a razor sharp focus that can easily become tunnel-vision. Blinkenlights solves this problem by using IBM Code Page 437. If we use it to visualize the same run-length encoded data above, and it's able to give us a better glance.

Please keep in mind, this is a purely intuitive display. It's going to look like gobbledygook to anyone who's unfamiliar with CP437, but surely anyone can agree it's better than a wall of period marks, in terms of the richness and complexity of the information it succinctly conveys. CP437 can be thought of as an alphabet with 256 letters. You can scroll through pages and pages of this stuff and your mind will magically spot and identify patterns. For example, you'll gain an intuition for what data does. For example, here's an indirect jump table:

Here's what a struct looks like when it's compiled with __attribute__((__packed__)):

Here's what x86-64 code looks like:

Here's what /dev/urandom looks like:

And here's what binaries built with UBSAN (Undefined Behavior Sanitizer) look like. As we can see, it's got plenty of room for improvement, and obviously explains why UBSAN binaries are so enormous. It's poor struct packing.

Cosmopolitan is an ex nihilo codebase. I started this project with an empty file and an assembler. Pretty much every byte that's gone into APE binaries since then, I've had some role in either creating and/or monitoring. As such, the two very first tools I wrote with Cosmopolitan Libc were intended to help me do just that.

-rwxr-xr-x 1 501 jart 52K Jun  9 09:08 bing.com (see bing.c)
-rwxr-xr-x 1 501 jart 32K Jun  9 09:08 fold.com (see fold.c)


I use them with the following shell script wrapper named ~/bin/bf.

#!/bin/sh
bing.com <"$1" |
  fold.com |
  exec less


So whenever I want to take a peek inside a file, I just type a command like:

bf o//examples/hello.com


I've written a few other scripts that come in handy. For instance, here's ~/bin/bloat which shows which symbols in a .com.dbg file are the biggest.

#!/bin/sh
nm -C --size "$@" |
  sort -r |
  grep ' [bBtTRr] ' |
  exec less

Field Arrangement

Struct packing is a nice wholesome size optimization that's not the least bit controversial. One good example is something I once noticed about Python 3.6 when viewing it through bing | fold. A core Python parser struct has suboptimal field arrangement.

typedef struct {
    int		 s_narcs;
    arc		*s_arc;
    int		 s_lower;
    int		 s_upper;
    int		*s_accel;
    int		 s_accept;
} state;


I wouldn't have noticed this if I was reading the code, since sometimes the stuff underneath the iceberg isn't always clear. That struct above, is actually equivalent to the following at the binary level:

typedef struct {
    int		 s_narcs;
    int		 __pad1;   // four wasted bytes
    arc		*s_arc;
    int		 s_lower;
    int		 s_upper;
    int		*s_accel;
    int		 s_accept;
    int		 __pad2;   // four wasted bytes
} state;


So I moved the s_accept field to a different line, and it shaved 4kb off every Python binary.

typedef struct {
    int		 s_narcs;
    int		 s_accept;
    arc		*s_arc;
    int		 s_lower;
    int		 s_upper;
    int		*s_accel;
} state;


Everything counts in small amounts. I also imagine there's some corporate styleguides at various companies where the latter code would be preferred, strictly for policy reasons. Since it's not great from a readability standpoint to have people scratching their heads wondering where the gaps are in your data structures, if they need assurances at the application binary interface level. So we're not only saving space but leading to better code hygeine too.

Run Length Encoding

There are so many outstanding compression algorithms in the news, based on machine learning and even classical algorithms, that I imagine many self-taught programmers might not be familiar with the really simple primitive ones that, in certain cases, get the job done. One such example is run-length encoding. The way it works, is if you have a sequence such as:

1,1,1,1,1,1,1,1,2,2,2,3


Then you'd encode it as sequence of {count, thing} tuples with a {0,0} terminator.

8,1, 3,2, 1,3, 0,0


What I love about run-length encoding is (1) it's so simple that the compressed data stream can be edited by hand; and (2) its decompressor only requires 14 bytes of code.

/	Fourteen byte decompressor.
/
/	@param	di points to output buffer
/	@param	si points to uint8_t {len₁,byte₁}, ..., {0,0}
/	@arch	x86-64,i386,i8086
/	@see	libc/nexgen32e/rldecode.S
rldecode:

31 c9
	xor	%ecx,%ecx

ac
0:	lodsb

86 c1
	xchg	%al,%cl

ac
	lodsb

e3 05
	jrcxz	2f

aa
1:	stosb

e2 fd
	loop	1b

eb f5
	jmp	0b

c3
2:	ret
	.type	rldecode,@function
	.size	rldecode,.-rldecode
	.globl	rldecode


ProTip: You can hover over instructions with a wavy line for an explanation of what it does.

That particular example is beautiful, since it's binary compatible with i8086, i386, and x86-64. However assembly doesn't always mean fast. For better explainability and performance, the following C code should do the trick:

struct RlDecode {
  uint8_t repititions;
  uint8_t byte;
};

void rldecode2(uint8_t *p, const struct RlDecode *r) {
  for (; r->repititions; ++r) {
    memset(p, r->byte, r->repititions);
    p += r->repititions;
  }
}


Run-length encoding is only appropriate for compressing sparse data. For denser data, RLE, will double its size! However it just so happens that, when we're making binaries smaller, there's usually many sparse data structures that can be efficiently run-length encoded.

One such example are the character translation tables used by the redbean web server, when parsing URIs and HTTP messages. One thing most C/C++ developers figure out eventually is that it's really efficient to perform a character lookup in a table with 256 entries. Why? Because your C compiler will turn C code like rdi[al & 255] into assembly that looks like this:

	movzbl	%al,%eax
	mov	(%rdi,%rax),%al


That's super fast, and memory safe too. Hardware engineers would call it a LookUp Table or LUT for short. It's quite integral to the workings of microprocessors. The x86 architecture even has a deprecated instruction called XLAT that's dedicated to this very thing. With HTTP, the most important use case for LUTs is to check if characters are legal. For example, many of the components of an HTTP message are required to be "tokens" quoth RFC2616:

CHAR           = <any US-ASCII character (octets 0 - 127)>
SP             = <US-ASCII SP, space (32)>
HT             = <US-ASCII HT, horizontal-tab (9)>
CTL            = <any US-ASCII control character
                 (octets 0 - 31) and DEL (127)>
token          = 1*<any CHAR except CTLs or separators>
separators     = "(" | ")" | "<" | ">" | "@"
               | "," | ";" | ":" | "\" | <">
               | "/" | "[" | "]" | "?" | "="
               | "{" | "}" | SP | HT


As plain C code, we could write our token LUT as follows:

const char kHttpToken[256] = {
   0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, // 0x00
   0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, // 0x10
   0, 1, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 0, // 0x20  ! #$%&‘  *+ -. 
   1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, // 0x30 0123456789      
   0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, // 0x40  ABCDEFGHIJKLMNO
   1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, // 0x50 PQRSTUVWXYZ   ^_
   1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, // 0x60 `abcdefghijklmno
   1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, // 0x70 pqrstuvwxyz | ~ 
   0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, // 0x80
   0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, // 0x90
   0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, // 0xa0
   0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, // 0xb0
   0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, // 0xc0
   0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, // 0xd0
   0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, // 0xe0
   0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, // 0xf0
};


That way we can just say kHttpToken[c & 255] to check if a character is valid in a token. But if we wanted to save 200 bytes of binary size, we could use run-length encoding.

	.globl	kHttpToken
	.section .bss.sort.100.kHttpToken,"aw",@nobits
/	@see	net/http/khttptoken.S
kHttpToken:
	.zero	256
	.section .rodata.sort.100.kHttpToken,"a",@progbits
	.byte	 33,0                   # 00-20 ∅-␠
	.byte	  1,1                   # 21-21 !-!
	.byte	  1,0                   # 22-22 “-“
	.byte	  5,1                   # 23-27 #-‘
	.byte	  2,0                   # 28-29 (-)
	.byte	  2,1                   # 2a-2b *-+
	.byte	  1,0                   # 2c-2c ,-,
	.byte	  2,1                   # 2d-2e --.
	.byte	  1,0                   # 2f-2f /-/
	.byte	 10,1                   # 30-39 0-9
	.byte	  7,0                   # 3a-40 :-@
	.byte	 26,1                   # 41-5a A-Z
	.byte	  3,0                   # 5b-5d [-]
	.byte	 29,1                   # 5e-7a ^-z
	.byte	  1,0                   # 7b-7b {-{
	.byte	  1,1                   # 7c-7c |-|
	.byte	  1,0                   # 7d-7d }-}
	.byte	  1,1                   # 7e-7e ~-~
	.byte	129,0                   # 7f-ff ⌂-λ
	.byte	0,0                     # terminator
	.section .init.sort.100.kHttpToken,"a",@progbits
	call	rldecode


There's a tool in the Cosmopolitan codebase for automatically generating these assembly files.

o//tool/build/xlat.com -TiC ' ()<>@,;:\"/[]?={}' -iskHttpToken

Decentralized Sections

The assembly code in the previous section that's generated by xlat.com might seem a bit strange, even for experienced x86 assembly programmers. It's a technique somewhat uniquely resurrected for Cosmopolitan, based on a reading of old code from the 70's and 80's. We'll call it "decentralized sections".

Decentralized sections are a way by which we can write a single function whose code spans multiple files. The canonical example of this, is the classic UNIX _init() function, which you'll find empty in nearly every modern codebase, because _init() is somewhat of a lost art intended to be assembled by the linker script.

The way this works is your libc defines the stubs for the prologue and epilogue of the _init() function. Here's how Cosmopolitan Libc defines it (with some slight edits to reduce macro usage in order to improve copy/pastability):

	.section .init_prologue,"ax",@progbits
	.globl	_init
/	@param	r12 is argc (still callee saved)
/	@param	r13 is argv (still callee saved)
/	@param	r14 is envp (still callee saved)
/	@param	r15 is envp (still callee saved)
/	@note	rdi is __init_bss_start (callee monotonic lockstep)
/	@note	rsi is __init_rodata_start (callee monotonic lockstep)
/	@see	libc/runtime/init.S
_init:	push	%rbp
	mov	%rsp,%rbp
	lea	__init_bss_start(%rip),%rdi
	lea	__init_rodata_start(%rip),%rsi
	.previous/*
	...
	decentralized content
	...
	*/.section .init_epilogue,"ax",@progbits
_woot:	leave
	ret
	.previous


Your libc also needs to declare stubs for the data sections. These technically could be declared in the linker script, but it's nicer to write them in a .S file so the symbols don't get defined unless they're being linked.

	.section .init_rodata_prologue,"a",@progbits
	.globl	__init_rodata_start,__init_rodata_end
	.align	__SIZEOF_POINTER__
__init_rodata_start:
	.previous/*
	...
	decentralized content
	...
	*/.section .init_rodata_epilogue,"a",@progbits
__init_rodata_end:
	.byte	0x90
	.previous

	.section .init_bss_prologue,"aw",@nobits
	.globl	__init_bss_start,__init_bss_end
	.align	__SIZEOF_POINTER__
__init_bss_start:
	.previous/*
	...
	decentralized content
	...
	*/.section .init_bss_epilogue,"aw",@nobits
__init_bss_end:
	.byte	0
	.previous



We then configure our linker script as follows:

/* see ape/ape.lds */
SECTIONS {
  .text . : {
    KEEP(*(.init_prologue))
    KEEP(*(SORT_BY_NAME(.init.sort.*)))
    KEEP(*(.init))
    KEEP(*(.init_epilogue))
    *(.text .text.*)
    KEEP(*(SORT_BY_NAME(.rodata.sort.*)))
    *(.rodata .rodata.*)
  }
  .bss . : {
    KEEP(*(SORT_BY_NAME(.bss.sort.*)))
    *(SORT_BY_ALIGNMENT(.bss))
    *(SORT_BY_ALIGNMENT(.bss.*))
    *(COMMON)
  }
}


It's now possible to write assembly files that insert content into the _init() function, along with the concomitant __init_rodata_start and __init_bss_start data structures. Both the read-only data and the uninitialized data (BSS) sections are optional. The only thing that's mandatory is that, unlike the normal System V Application Binary Interface, our _init() code isn't allowed to clobber RDI and RSI. Because they store lockstep pointers to the rodata and bss.

Here's an example than of how it can be used, that's simpler than the kHttpToken example above. Let's say I need to support the AMD K8 aand Barcelona microarchitectures, but I want to take advantage of SSSE3 (which is the best SSE). The industry practice here is to perform a CPUID check behind a double-checked pthread_once() guard, because the CPUID instruction takes 50 nanoseconds each time, whereas the once guard averages out over many calls to cost half a nanosecond. However the _init() function provides a better solution, since it obfuscates the need for synchronization libraries, due to how _init() is called before all other constructors, thereby making it highly unlikely that any threads to have been created.

	.section .bss.sort.100.kCpuid1,"aw",@nobits
/	uint32_t kCpuid1[4];
/	@see	libc/nexgen32e/kcpuids.S
kCpuid1:.long	0,0,0,0
	.globl	kCpuid1
	.type	kCpuid1,@object
	.size	kCpuid1,.-kCpuid1

	.section .init.sort.100.kCpuid1,"a",@progbits

53
	push	%rbx

6a 01
	push	$1

58
	pop	%rax

0f a2
	cpuid

ab
	stosl

93
	xchg	%eax,%ebx

ab
	stosl

91
	xchg	%eax,%ecx

ab
	stosl

92
	xchg	%eax,%edx

ab
	stosl

5b
	pop	%rbx


Note: If you've ever felt mystified by Intel's marketing and wondered which CPUs have which features based on their true microarchitectural name, then there's an executive summary in microarch.txt.

The code above only adds 14 bytes of content to the binary. It scales in terms of development model; any number of libraries throughout your codebase can follow this process without stepping on each others toes. As a model, decentralized sections really gives us a sweet spot that caters to the gigantic codebases big companies respect, while creating the tiny binaries indie developers adore. It's also much lighter weight than needing to pull in a dependency on -lpthread. Now, when I want to check if SSSE3 is available, all I have to do is check if the 9th bit of the ECX we stored earlier is set:

if (kCpuid1[2][1<<9]) {
  // we have ssse3!
} else {
  // it's k8 or barcelona
}


If you're using a different libc from cosmo (e.g. musl, glibc) then you can still use this same technique, today, with some slight alteration.

	.bss
kCpuid1:.long	0,0,0,0
	.globl	kCpuid1
	.type	kCpuid1,@object
	.size	kCpuid1,.-kCpuid1

	.section .init,"a",@progbits

53
	push	%rbx

48 8d 3d 00 00 00 00
	lea	kCpuid1(%rip),%rdi

6a 01
	push	$1

58
	pop	%rax

0f a2
	cpuid

ab
	stosl

93
	xchg	%eax,%ebx

ab
	stosl

91
	xchg	%eax,%ecx

ab
	stosl

92
	xchg	%eax,%edx

ab
	stosl

5b
	pop	%rbx


Here we need to pay for 7 additional bytes (21 bytes total), because the lockstep cooperation between _init() / rodata / bss is unique to Cosmo and not implemented by other C libraries. But in either case, both assembly solutions are a clear win over the C/C++ equivalent, which needs 42 bytes.

uint32_t kCpuid1[4];

__attribute__((__constructor__)) static void kCpuid1Init() {
  uint32_t ax, bx, cx, dx;
  asm("cpuid" : "=a"(ax), "=b"(bx), "=c"(cx), "=d"(dx) : "0"(1));
  kCpuid1[0] = ax;
  kCpuid1[1] = bx;
  kCpuid1[2] = cx;
  kCpuid1[3] = dx;
}


Note: If you're bewildered by the Richard Stallman Math 55 notation used by the asm() keyword, you can find an executive summary in rmsiface.txt.

If there's one thing I've learned working on Cosmopolitan, it's that with the right finesse, the C compiler can produce really tiny code if we're willing to write assembly inside string literals. The following code shows how to get GCC and Clang to do it in 30 bytes. Whether or not it's worth it versus just writing assembly is up to the reader.

uint32_t kCpuid1[4];

__attribute__((__constructor__)) static void kCpuid1Init() {
  uint32_t ax, *di;
  asm volatile("cpuid\r\n"
               "stosl\r\n"
               "xchg\t%%ebx,%%eax\r\n"
               "stosl\r\n"
               "xchg\t%%ecx,%%eax\r\n"
               "stosl\r\n"
               "xchg\t%%edx,%%eax\r\n"
               "stosl"
               : "=a"(ax), "=D"(di)
               : "0"(1), "1"(kCpuid1)
               : "rbx", "rcx", "rdx", "memory");
}


The main thing that makes the C code clunkier is it needs to generate an 8 byte function pointer in a .ctors section which needs to be added to the linker script separately. Your C library will normally call ctors after _init() is finished. There really aren't any acceptable solutions for getting a modern C compiler to generate "decentralized section" style code. The closest we can get is the following, using GCC (but certainly not Clang, which claims dominion over all registers).

register long di asm("rdi");
register long si asm("rsi");

__attribute__((__section__(".bss.sort.100.kCpuid1,\"aw\",@nobits #")))
uint32_t kCpuid1[4];

__attribute__((__used__,
               __section__(".init.sort.100.kCpuid1,\"a\",@progbits #")))
static void kCpuid1Init(void) {
  uint32_t ax;
  asm volatile("push\t%%rbx\r\n"
               "cpuid\r\n"
               "stosl\r\n"
               "xchg\t%%ebx,%%eax\r\n"
               "stosl\r\n"
               "xchg\t%%ecx,%%eax\r\n"
               "stosl\r\n"
               "xchg\t%%edx,%%eax\r\n"
               "stosl\r\n"
               "push\t%%rbx"
               : "=a"(ax), "+D"(di)
               : "0"(1)
               : "rcx", "rdx", "memory");
  __builtin_unreachable();  // prevent generation of RET instruction
}


The problem with the above code is it's brittle. You need to pass compiler flags like -ffixed-rdi -ffixed-rsi -fomit-frame-pointer -O -fno-sanitize=all for it to work properly. The value of a C compiler is being able to bloat our code with debugging tools (like ASAN) when we want them. So with code like this, where that can't happen, it's usually best to just write assembly.

Dead Code Elimination

Naturally, if you're a Cosmopolitan Libc user, all the stuff in the CPUID examples above would would be taken care of for you, and you need to say is this:

// see libc/nexgen32e/x86feature.h
if (X86_HAVE(SSSE3)) {
  // we have ssse3!
} else {
  // it's k8 or barcelona
}


It's worth taking a look at its implementation in x86feature.h since it's quite possibly the most beautiful abstraction created with the C preprocessor you're likely to find in the entire codebase. It also embodies one of the most important patterns of Cosmopolitan macros, which is the hybridization of compile-time and runtime checking. It's needed by Actually Portable Executable (which relies heavily on runtime dispatch) while still granting all the traditional compile-time define flag tuning that developers love. For example, the #ifdef model could be implemented here as follows:

#if X86_REQUIRE(SSSE3)
  // we have ssse3!
#else
  // it's k8 or barcelona
#endif


In that case, your program can only support SSSE3 if the user passes the -mssse3 flag to the compiler. It's better to use the X86_HAVE() macro because it does the same thing as X86_REQUIRE(SSSE3) except it has a runtime check too. By default, if you pass no microarchitecture flags to GCC or Clang, both branches get included in the binary.

if (X86_HAVE(SSSE3)) {
  // do some wild ssse3 assembly hacks
} else {
  // fallback to slow ansi c code
}


But if the user chooses to pass the -mssse3 flag, then the fallback bloat for supporting old CPU models gets removed by a compiler optimization pass, along with the runtime check itself.

if (X86_HAVE(SSSE3)) {
  // do some wild ssse3 assembly hacks
} else {
  // fallback to slow ansi c code
}


This is what MODE=opt does with the Makefile build config by default. It passes the -march=native flag to the compiler, which asks it to figure out what features the CPU in your host machine has, and then Cosmopolitan and GCC work together to produce a binary that's just right and optimally fast your machine. The tradeoff is you won't be able to distribute any such binaries, since they might not run on other x86 CPU models.

The basic idea behind how the hybrid model to dead code elimination and runtime branching works, is most simply and elegantly expressed in ape/loader.c and libc/dce.c.

#define LINUX   1
#define METAL   2
#define WINDOWS 4
#define XNU     8
#define OPENBSD 16
#define FREEBSD 32
#define NETBSD  64

#define SupportsLinux()   (SUPPORT_VECTOR & LINUX)
#define SupportsXnu()     (SUPPORT_VECTOR & XNU)
#define SupportsFreebsd() (SUPPORT_VECTOR & FREEBSD)
#define SupportsOpenbsd() (SUPPORT_VECTOR & OPENBSD)
#define SupportsNetbsd()  (SUPPORT_VECTOR & NETBSD)

#define IsLinux()   (SupportsLinux() && os == LINUX)
#define IsXnu()     (SupportsXnu() && os == XNU)
#define IsFreebsd() (SupportsFreebsd() && os == FREEBSD)
#define IsOpenbsd() (SupportsOpenbsd() && os == OPENBSD)
#define IsNetbsd()  (SupportsNetbsd() && os == NETBSD)


So one of the flexibilities of APE is the build can be tuned like this:

make MODE=tiny CPPFLAGS+=-DSUPPORT_VECTOR=0b00000001


If you want a 4kb hello world binary that only runs on Linux, and leaves out that hefty 12kb of bloat that's normally included to support Windows, MacOS, FreeBSD, NetBSD, OpenBSD, and booting from BIOS on bare metal. One sweet spot is to only target the ELF operating systems. Simply set the appropriate bits for Linux + BSD.

make MODE=tiny CPPFLAGS+=-DSUPPORT_VECTOR=0b01110001

δzd Encoding

One of the most size optimized pieces of code in the Cosmopolitan codebase is Python. This is where we really had to go beyond code golfing and pull out the artillery when it comes to size coding. One of the greatest weapons in our arsenal (which helped us get statically linked Python binaries down to 2mb in size) is what we call the Delta Zig-Zag Deflate compression scheme, or δzd for short.

This isn't a generalized compression algorithm like DEFLATE, which employs Huffman coding (along with an RLE very similar to LZ4). It's only profitable on certain kinds of executable content and while programming we need to use our best judgement to figure out which technique is most appropriate. But δzd in particular has produced some considerable gains.

Consider the following dilemma. The Chinese, Korean, and Japanese languages are enormous. They don't even all agree on UTF-8 yet, and have a variety of one-off character sets, all of which are supported by Python. The UNICODE standard and its information tables also need to be enormous too, in order to support CJK. Most people outside those three countries don't need this information in their binaries, but we like to keep it there anyway, in the interest of inclusiveness and enabling languages like Python to erect a big tent that welcomes everyone.

By using δzd packing, we can make these lookup tables significantly tinier, thereby ensuring that the user only needs to pay for the features they actually use. One of the many symbols in the Python codebase that needed this treatment is _PyUnicode_PhrasebookOffset2 which was originally 178kb in size, but apply delta encoding, zig-zag encoding, and then finally DEFLATE, we got it down to 12kb. That's a nearly 10x advantage over DEFLATE's Huffman encoding alone, and BZIP2's Burrows-Wheeler transform!

_PyUnicode_PhrasebookOffset2: size         is      178,176 bytes
_PyUnicode_PhrasebookOffset2: packed size  is      100,224 bytes
_PyUnicode_PhrasebookOffset2: rle size     is      282,216 bytes
_PyUnicode_PhrasebookOffset2: deflate size is       52,200 bytes
_PyUnicode_PhrasebookOffset2: bz2 size     is       76,876 bytes
_PyUnicode_PhrasebookOffset2: δleb size    is       47,198 bytes
_PyUnicode_PhrasebookOffset2: δzd size     is       12,748 bytes


In third_party/python/Tools/unicode/makeunicodedata.py you can read more about how we regenerated these tables. The Python implementation for Delta-ZigZag-DEFLATE encoding is also as follows:

def uleb(a, x):
    while True:
        b = x & 127
        x >>= 7
        if x:
            a.append(b | 128)
        else:
            a.append(b)
            break

def zig(x):
    m = (2 << x.bit_length()) - 1
    return ((x & (m >> 1)) << 1) ^ (m if x < 0 else 0)

def zleb(a, x):
    return uleb(a, zig(x))

def δzd(data):
    n = 0;
    i = 0
    p = 0
    a = bytearray()
    for x in data:
        zleb(a, x - p)
        p = x
    return deflate(a), len(a)


You can read the C code that unpacks the Python compressed data in libc/x/xloadzd.c, libc/fmt/unzleb64.c, libc/runtime/inflate.c, and third_party/zlib/puff.c. Puff is particularly nice. It's a size optimized (but slower) version of zlib that Mark Adler wrote that only does DEFLATE decompression, and it has a binary footprint of 2kb. One thing Cosmopolitan Libc core libraries do quite frequently (since they can't depend on things like malloc) whenever the need arises for proper DEFLATE decompression, is strongly link Puff, and weakly link zlib (which is more on the order of 60kb in size) so that Puff is used by default, unless the faster zlib library is strongly linked by something else.

Overlapping Functions

If high-level programming languages like C are the Ice Hotel and assembly is the tip of the iceberg, then the hidden dimension of complexity lurking beneath would be Intel's variable length encoding. This is where boot sectors get esoteric real fast, since tools can't easily visualize it. for example, consider the following:

/	%ip is 0
	mov	$0xf4,%al
	ret

	
/	%ip is 1
	.byte	0xb0
wut:	hlt # and catch fire
	ret


Similar to how a Chess game may unfold very differently if a piece is moved to an unintended adjacent square, an x86 program can take on an entirely different meaning if the instruction pointer becomes off by one. We were able to use this to our advantage, since that lets us code functions in such a way that they overlap with one another.

/	SectorLISP code.

89 D6
 Assoc:	mov	%dx,%si

8B 3C
 1:	mov	(%si),%di

8B 30
 	mov	(%bx,%si),%si

AF   
 	scasw

75 F9
 	jne	1b

F6   
 	.byte	0xF6

8B 39
 Cadr:	mov	(%bx,%di),%di

3C   
 	.byte	0x3C

AF   
 Cdr:	scasw

8B 05
 Car:	mov	(%di),%ax

C3   
 	ret

	
89 D6         
 Assoc:	mov	%dx,%si

8B 3C         
 1:	mov	(%si),%di

8B 30         
 	mov	(%bx,%si),%si

AF            
 	scasw

75 F9         
 	jne	1b

F6 8B 39 3C AF
 	testw	$0xaf,0x3c39(%bp,%di)

8B 05         
 	mov	(%di),%ax

C3            
 	ret


8B 39         
 Cadr:	mov	(%bx,%di),%di

3C AF         
 	cmp	$0xaf,%al

8B 05         
 	mov	(%di),%ax

C3            
 	ret


AF            
 Cdr:	scasw

8B 05         
 	mov	(%di),%ax

C3            
 	ret


8B 05         
 Car:	mov	(%di),%ax

C3            
 	ret

Optimizing Printf

One of the issues with printf() from a size coding perspective, is it pulls in a lot of heavy-weight dependencies:

gdtoa is needed to format double and long double via %f, %g, etc. There's so much depth (and potentially memory allocation) when it comes to formatting floating point. As such, linking gdtoa adds about 32kb to the binary size.
In order to format width-aligned strings (via %*s etc.) in a way that supports UNICODE, we need the CJK wides table, which lets us know if a character in the terminal takes up two cells. Some such examples of variable width monospace would be Emoji and Chinese.
Formatting the GNU %m directive for strerror() is a little more costly with Cosmopolitan, because we use symbols rather than defines for system magic numbers. Therefore strerror() needs to yoink all the errnos at once. It also needs to embed a bunch of error string and tools for obtaining them via the WIN32 API. It adds about ~8k to the binary size.

Yet somehow, despite all the bloat in printf(), binaries that casually link it (e.g. examples/hello3.c) can be as small as 24kb in size. This is thanks to the PFLINK() macro.

/* see libc/fmt/pflink.h */
/* see libc/stdio/stdio.h */
#define printf(FMT, ...) (printf)(PFLINK(FMT), ##__VA_ARGS__)
#define PFLINK(...) _PFLINK(__VA_ARGS__)
#define _PFLINK(FMT, ...)                                             \
  ({                                                                  \
    if (___PFLINK(FMT, strpbrk, "faAeg")) STATIC_YOINK("__fmt_dtoa"); \
    if (___PFLINK(FMT, strpbrk, "cmrqs")) {                           \
      if (___PFLINK(FMT, strstr, "%m")) STATIC_YOINK("strerror");     \
      if (!IsTiny() && (___PFLINK(FMT, strstr, "%*") ||               \
                        ___PFLINK(FMT, strpbrk, "0123456789"))) {     \
        STATIC_YOINK("strnwidth");                                    \
        STATIC_YOINK("strnwidth16");                                  \
        STATIC_YOINK("wcsnwidth");                                    \
      }                                                               \
    }                                                                 \
    FMT;                                                              \
  })
#define ___PFLINK(FMT, FN, C) \
  !__builtin_constant_p(FMT) || ((FMT) && __builtin_##FN(FMT, C) != NULL)


This only works with GCC and not Clang. It works because the first argument to printf() is almost always a string literal, and GCC is smart enough to run functions like __builtin_strstr() at compile time, sort of like a C++ constexpr. Once GCC has identified that we need a heavyweight feature, it then does what we call "yoinking" the appropriate symbol.

Here's how yoinking works. There's a trick with ELF binaries called weak linking. The printf() implementation has code like this:

      case 'm':
        p = weaken(strerror) ? weaken(strerror)(lasterr) : "?";
        signbit = 0;
        goto FormatString;


When a function is weakened, then it won't get pulled into the final binary unless some other module references it the strong or normal way. Yoinking is one way to do that. However yoinking is intended for the special situation where don't have any code that actually uses the symbol, but we still want to pull it into the binary.

	.section .yoink
	nopl	symbol
	.previous


So what we do with the yoink macro is is generate a reference inside a section that's explicitly discarded by the linker script.

  /DISCARD/ : {
    *(.yoink)
  }


So even though that reference is ultimately discarded, it's still enough to cause ld.bfd to pull the referenced module into the final binary.

This isn't a perfect technique, even though it's a worthwhile one. Large programs will implicitly yoink everything on a long enough timeline. So for big programs, this isn't a problem. But it's sometimes necessary for tiny programs to help the linker out explicitly. For example, you may be committing the security sin of using non-literal format strings. In that case the macro magic will cause everything to be yoinked, since it has no visibility into the string at compile time. If you still want to stay on the tinier side, then you can disable the magic by calling printf() as such:

(printf)("last error is %m\n");

Then, any features you need which are listed in the PFLINK() macro can be yoinked explicitly by your main() module.
STATIC_YOINK("strerror");

Tiny Portable ELF

Please take a look at the How Fat Does a Fat Binary Need To Be? page which lets you interactively build online Cosmopolitan Actually Portable Executable binaries. As we can see, features like SUPPORT_VECTOR provide all the power and configurability any user should need, to make their programs as tiny as they want them to be.

But let's say for a moment you only cared about ELF targets like Linux, FreeBSD, NetBSD, and OpenBSD. Let's furthermore imagine that you wanted to build a binary that runs on all four of these operating systems, from scratch, without the assistance of APE and Cosmo. It turns out that's relatively easy to do, and this section will show you how it works. What's also cool is that it's only 386 bytes in size, using an idiomatic best practices approach.

Throughout the history of computing, it's been convention that each operating systems should provide its own tools that let you build software for the platform. This made sense in the past, since operating systems were usually built by the same companies that designed the microprocessors on which they operated. Things changed in recent decades. As of August 2022, 485 out of the Top 500 supercomputers run x86-64. The x86 architecture also represents the lion's share of personal computers and backend servers. Yet, due to tradition, programmers still believe that if we want to release an app for four different operating systems, we need to build four separate binaries. That doesn't make sense anymore, because all four binaries share the same architecture.

For example, let's say you build the following function:

int add(int x, int y) {
  return x + y;
}


The output of your compiler should be the same, regardless of whether you're running on Linux, FreeBSD, NetBSD, or OpenBSD:

add:	lea	(%rdi,%rsi,1),%eax
	ret


So why doesn't something like a Linux binary run out of the box on other systems like OpenBSD? There are a few reasons. First, the ELF format itself requires us to specify the OS ABI (convention for how functions interact at a binary/register level). Fortunately we can get around this by just setting it to the FreeBSD ABI. This is because FreeBSD is the only UNIX operating system that checks this field. It turned out that NetBSD and OpenBSD check for binary compatibility using a separate ELF PT_NOTE data structure instead. As for Linux, it just doesn't care. So it turns out, if we say it's a FreeBSD binary, and we put the NetBSD and OpenBSD notes in there too, then our binary will run on all four.

There's a few other minor differences in how the operating systems interpret ELF fields. For example, PT_LOAD is used to tell the operating system which parts of the executable file should be loaded into memory, and at which addresses they should reside. These PT_LOAD segments are allowed to have a size of zero, in terms of the file. That's basically equivelent to allocating zero'd memory. However if the size in memory is zero too, then OpenBSD will refuse to run the progarm, whereas the other kernels just don't care.

The executable header incantations below are designed to walk the narrow path that meets the intersection of requirements for all four operating systems. They'll then load our identical x86 code into memory, and run it.

/* reallytiny-elf.S */
#define ELFCLASS64 2
#define ELFDATA2LSB 1
#define ELFOSABI_FREEBSD 9
#define ET_EXEC 2
#define EM_NEXGEN32E 62
#define PT_LOAD 1
#define PT_NOTE 4
#define PF_X 1
#define PF_W 2
#define PF_R 4

	.align	8
ehdr:	.ascii	"\177ELF"
	.byte	ELFCLASS64
	.byte	ELFDATA2LSB
	.byte	1
	.byte	ELFOSABI_FREEBSD
	.quad	0
	.word	ET_EXEC			# e_type
	.word	EM_NEXGEN32E		# e_machine
	.long	1			# e_version
	.quad	_start			# e_entry
	.quad	phdrs - ehdr		# e_phoff
	.quad	0			# e_shoff
	.long	0			# e_flags
	.word	64			# e_ehsize
	.word	56			# e_phentsize
	.word	2			# e_phnum
	.word	0			# e_shentsize
	.word	0			# e_shnum
	.word	0			# e_shstrndx
	.globl	ehdr

	.align	8
phdrs:	.long	PT_LOAD			# p_type
	.long	PF_R|PF_X		# p_flags
	.quad	0			# p_offset
	.quad	ehdr			# p_vaddr
	.quad	ehdr			# p_paddr
	.quad	filesz			# p_filesz
	.quad	filesz			# p_memsz
	.quad	64			# p_align

#if 0  // will break openbsd unless we actually use bss
	.long	PT_LOAD			# p_type
	.long	PF_R|PF_W		# p_flags
	.quad	0			# p_offset
	.quad	bss			# p_vaddr
	.quad	bss			# p_paddr
	.quad	0			# p_filesz
	.quad	bsssize			# p_memsz
	.quad	64			# p_align
#endif

	.long	PT_NOTE			# p_type
	.long	PF_R			# p_flags
	.quad	note - ehdr		# p_offset
	.quad	note			# p_vaddr
	.quad	note			# p_paddr
	.quad	notesize		# p_filesz
	.quad	notesize		# p_memsz
	.quad	8			# p_align

note:	.long	2f-1f
	.long	4f-3f
	.long	1
1:	.asciz	"OpenBSD"
2:	.align	4
3:	.long	0
4:	.long	2f-1f
	.long	4f-3f
	.long	1
1:	.asciz	"NetBSD"
2:	.align	4
3:	.long	901000000
4:	notesize = . - note

_start:	mov	%rsp,%rsi
	jmp	Start
	.globl	_start



At that point we can just put our code in the Start() function and it'll work! But a second issue occurs when we actually want to print the result.

To print a string on UNIX systems, we must invoke the int write(fd, data, size) system call, where fd is normally specified as 1, which means standard output. Once again, due to the similarities of the post-shakeout operating system landscape, all four systems happen to implement the exact same function. However, in order to actually call it, there's another number we must specify that exists beneath the iceberg of what we see in terms of C code. That number is the system call magic number, or "magnum", and it's part of what's known as the Application Binary Interface (ABI). Unfortunately, operating systems don't agree on magnums. For example, on Linux write() is 1, but on the BSDs it's 4. So if we ran Linux's write() on BSD, it would actually call exit() – not what we want!

UNIX SYSCALL Magnums (x86-64)
Function	Linux	FreeBSD	OpenBSD	NetBSD
exit	60	1	1	1
fork	57	2	2	2
read	0	3	3	3
write	1	4	4	4
open	2	5	5	5
close	3	6	6	6
stat	4	n/a	38	439
fstat	5	551	53	440
poll	7	209	252	209

You'll notice there's a subset of numbers on which all systems agree, particularly among the BSDs. Those tend to be the really old functions that were designed for the original UNIX operating system written at Bell Labs. In fact, numbers such as 1 for exit() were copied straight out of the Bell System Five codebase. That's why we call it the System V Application Binary Interface. There even used to be more consensus if we look at past editions.

UNIX SYSCALL Magnums (i386)
Function	Linux	FreeBSD	OpenBSD	NetBSD
exit	1	1	1	1
fork	2	2	2	2
read	3	3	3	3
write	4	4	4	4
open	5	5	5	5
close	6	6	6	6
stat	18	n/a	38	439
fstat	108	551	53	440
poll	168	209	252	209

So in order to know which magnum to use, we need some way of detecting the x86-64 OS at runtime. There's many ways of doing this. For example, we could search for a magnum where we pass invalid parameters and then tell the systems apart by the returned error code. However system calls are costly, taking upwards of a microsecond to execute, rather than nanoseconds like ordinary functions. So we'll be showing a different technique below, which detects the operating system based entirely on values that've already been passed to us by the operating system when it loaded our executable.

/* reallytiny.c */
#define LINUX   1
#define OPENBSD 16
#define FREEBSD 32
#define NETBSD  64

#ifndef SUPPORT_VECTOR
#define SUPPORT_VECTOR (LINUX | FREEBSD | NETBSD | OPENBSD)
#endif

#define SupportsLinux()   (SUPPORT_VECTOR & LINUX)
#define SupportsFreebsd() (SUPPORT_VECTOR & FREEBSD)
#define SupportsOpenbsd() (SUPPORT_VECTOR & OPENBSD)
#define SupportsNetbsd()  (SUPPORT_VECTOR & NETBSD)

#define IsLinux()   (SupportsLinux() && os == LINUX)
#define IsFreebsd() (SupportsFreebsd() && os == FREEBSD)
#define IsOpenbsd() (SupportsOpenbsd() && os == OPENBSD)
#define IsNetbsd()  (SupportsNetbsd() && os == NETBSD)

__attribute__((__noreturn__)) static void Exit(int rc, int os) {
  asm volatile("syscall"
               : /* no outputs */
               : "a"(IsLinux() ? 60 : 1), "D"(rc)
               : "memory");
  __builtin_unreachable();
}

static int Write(int fd, const void *data, int size, int os) {
  char cf;
  int ax, dx;
  asm volatile("clc\n\t"
               "syscall"
               : "=a"(ax), "=d"(dx), "=@ccc"(cf)
               : "0"(IsLinux() ? 1 : 4), "D"(fd), "S"(data), "1"(size)
               : "rcx", "r11", "r8", "r9", "r10", "memory", "cc");
  if (cf) ax = -ax;
  return ax;
}

static int Main(int argc, char **argv, char **envp, long *auxv, int os) {
  Write(1, "hello world\n", 12, os);
  return 0;
}

__attribute__((__noreturn__)) void Start(long di, long *sp) {
  long *auxv;
  int i, os, argc;
  char **argv, **envp, *page;

  // detect freebsd
  if (SupportsFreebsd() && di) {
    os = FREEBSD;
    sp = (long *)di;
  } else {
    os = 0;
  }

  // extract arguments
  argc = *sp;
  argv = (char **)(sp + 1);
  envp = (char **)(sp + 1 + argc + 1);
  auxv = (long *)(sp + 1 + argc + 1);
  for (;;) {
    if (!*auxv++) {
      break;
    }
  }

  // detect openbsd
  if (SupportsOpenbsd() && !os && !auxv[0]) {
    os = OPENBSD;
  }

  // detect netbsd
  if (SupportsNetbsd() && !os) {
    for (; auxv[0]; auxv += 2) {
      if (auxv[0] == 2014 /* AT_EXECFN */) {
        os = NETBSD;
        break;
      }
    }
  }

  // default operating system
  if (!os) {
    os = LINUX;
  }

  Exit(Main(argc, argv, envp, auxv, os), os);
}


FreeBSD likes to have %RDI (which means first parameter in System V ABI) be the same as %RSP on initialization. That's because they prefer C code, and don't want to require that people write the assembly thunk we did earlier, that moves the %RSP register and jumps to the real entrypoint. On the other operating systems, %RDI is always zero.

We then have to scrape the real parameters to our function off the stack. That's because x86-64 _start() is a weird function that still follows the old i386 ABI, which passed parameters on the stack (rather than in registers). Now we have argc, argv, and environ.

However there's a little known fourth parameter to C programs, called auxv, which is short for auxiliary values. OpenBSD never implemented this feature, so if they're not there, then we know it's OpenBSD. As for NetBSD, we know it always passes auxiliary values with much larger magnums than any other system, so by testing the values, we can tell NetBSD apart from Linux. Then we're done! We can now issues SYSCALLs.

But there's one more minor problem. BSDs don't conform to the System V ABI documentation, which says that error numbers should be returned by the kernel as a negative number. BSDs instead follow the the 386BSD convention of using the carry flag to indicate that RAX contains an error code instead of a result. Since we know that Linux always saves and restores the EFLAGS register during SYSCALL, all we have to do is use CLC to clear the carry flag before using SYSCALL. Then we know for certain that if the carry flag is set afterwards, that it's BSD and the SYSCALL failed, in which case we just flip the sign to make the result conform to System V.

There's some other quirks too. In our inline asm notation, we tell GCC that the the RDX register may be clobbered. This can only happen on XNU and NetBSD, but never on Linux, and highly unlikely on the other ones. FreeBSD usually clobbers R8, R9, and R10. It's generally best to assume with BSDs that they want you to wrap SYSCALL with a function call, so the call-clobbered register rule applies, i.e. RAX, RCX, RDX, RDI, RSI, R8, R9, R10, and R11 are volatile. BSDs system calls in some cases might even accept parameters on the stack, whereas Linux never uses more than six parameters, all of which go in the registers RDI, RSI, RDX, R10, R8, and R9.

Now that we've written all our code, we need a linker script to glue our C and assembly code together into a simple binary file, that doesn't have any of the platform-specific boilerplate.

/* reallytiny.lds */
ENTRY(_start)

SECTIONS {
  . = 0x400000;
  .text : {
    *(.text)
    *(.rodata .rodata.*)
  }
  filesz = . - ehdr;
  textsz = . - _start;
  .bss ALIGN(4096) : {
    bss = .;
    *(.bss)
    . = ALIGN(4096);
  }
  memsz = . - ehdr;
  /DISCARD/ : {
    *(.*)
  }
}

bsssize = SIZEOF(.bss);
textoff = _start - ehdr;


You can then build your program as such:

gcc -static -no-pie -g -Os \
  -o reallytiny.elf.dbg \
  -Wl,-T,reallytiny.lds \
  reallytiny-elf.S \
  reallytiny.c
objcopy -S -O binary \
  reallytiny.elf.dbg \
  reallytiny.elf


Here's your binary visualized:

Here's what happens when you run it:

linux$ ./reallytiny.elf
hello world
freebsd$ ./reallytiny.elf
hello world
netbsd$ ./reallytiny.elf
hello world
openbsd$ ./reallytiny.elf
hello world


Four operating systems is under 400 bytes is pretty good!

You may also download the examples above in the following files:

reallytiny-elf.S
reallytiny.c
reallytiny.lds
Funding

Funding for this blog post was crowdsourced from Justine Tunney's GitHub sponsors and Patreon subscribers. Your support is what makes projects like Cosmopolitan Libc possible. Thank you.

See Also
cosmopolitan libc
justine's web page
twitter.com/justinetunney

github.com/jart

Written by Justine Tunney

jtunney@gmail.com
