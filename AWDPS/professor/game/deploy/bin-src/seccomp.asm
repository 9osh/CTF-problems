# check if arch is X86_64
A = arch
A == ARCH_X86_64 ? next : dead
A = sys_number
A >= 0x40000000 ? dead : next
A == seccomp ? dead : next
A == ptrace ? dead : next
A == prctl ? dead : next
A == fork ? dead : next
A == vfork ? dead : next
A == kill ? dead : ok
return ERRNO(5)
ok:
return ALLOW
dead:
return KILL
