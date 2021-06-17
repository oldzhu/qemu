/*
 * Internal execution defines for qemu
 *
 *  Copyright (c) 2003 Fabrice Bellard
 *
 * SPDX-License-Identifier: LGPL-2.1-or-later
 */

#ifndef ACCEL_TCG_INTERNAL_H
#define ACCEL_TCG_INTERNAL_H

#include "exec/exec-all.h"

TranslationBlock *tb_gen_code(CPUState *cpu, target_ulong pc,
                              target_ulong cs_base, uint32_t flags,
                              int cflags);

void QEMU_NORETURN cpu_io_recompile(CPUState *cpu, uintptr_t retaddr);
<<<<<<< HEAD
=======
void page_init(void);
void tb_htable_init(void);
>>>>>>> 38848ce565849e5b867a5e08022b3c755039c11a

#endif /* ACCEL_TCG_INTERNAL_H */
