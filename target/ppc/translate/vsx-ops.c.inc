GEN_HANDLER_E(mfvsrwz, 0x1F, 0x13, 0x03, 0x0000F800, PPC_NONE, PPC2_VSX207),
GEN_HANDLER_E(mtvsrwa, 0x1F, 0x13, 0x06, 0x0000F800, PPC_NONE, PPC2_VSX207),
GEN_HANDLER_E(mtvsrwz, 0x1F, 0x13, 0x07, 0x0000F800, PPC_NONE, PPC2_VSX207),
#if defined(TARGET_PPC64)
GEN_HANDLER_E(mfvsrd, 0x1F, 0x13, 0x01, 0x0000F800, PPC_NONE, PPC2_VSX207),
GEN_HANDLER_E(mtvsrd, 0x1F, 0x13, 0x05, 0x0000F800, PPC_NONE, PPC2_VSX207),
GEN_HANDLER_E(mfvsrld, 0X1F, 0x13, 0x09, 0x0000F800, PPC_NONE, PPC2_ISA300),
GEN_HANDLER_E(mtvsrdd, 0X1F, 0x13, 0x0D, 0x0, PPC_NONE, PPC2_ISA300),
GEN_HANDLER_E(mtvsrws, 0x1F, 0x13, 0x0C, 0x0000F800, PPC_NONE, PPC2_ISA300),
#endif

#define GEN_XX1FORM(name, opc2, opc3, fl2)                              \
GEN_HANDLER2_E(name, #name, 0x3C, opc2 | 0, opc3, 0, PPC_NONE, fl2), \
GEN_HANDLER2_E(name, #name, 0x3C, opc2 | 1, opc3, 0, PPC_NONE, fl2)

#define GEN_XX2FORM(name, opc2, opc3, fl2)                           \
GEN_HANDLER2_E(name, #name, 0x3C, opc2 | 0, opc3, 0, PPC_NONE, fl2), \
GEN_HANDLER2_E(name, #name, 0x3C, opc2 | 1, opc3, 0, PPC_NONE, fl2)

#define GEN_XX2FORM_EXT(name, opc2, opc3, fl2)                          \
GEN_HANDLER2_E(name, #name, 0x3C, opc2 | 0, opc3, 0x00100000, PPC_NONE, fl2), \
GEN_HANDLER2_E(name, #name, 0x3C, opc2 | 1, opc3, 0x00100000, PPC_NONE, fl2)

#define GEN_XX2FORM_EO(name, opc2, opc3, opc4, fl2)                          \
GEN_HANDLER2_E_2(name, #name, 0x3C, opc2 | 0, opc3, opc4, 0, PPC_NONE, fl2), \
GEN_HANDLER2_E_2(name, #name, 0x3C, opc2 | 1, opc3, opc4, 0, PPC_NONE, fl2)

#define GEN_XX3FORM(name, opc2, opc3, fl2)                           \
GEN_HANDLER2_E(name, #name, 0x3C, opc2 | 0, opc3, 0, PPC_NONE, fl2), \
GEN_HANDLER2_E(name, #name, 0x3C, opc2 | 1, opc3, 0, PPC_NONE, fl2), \
GEN_HANDLER2_E(name, #name, 0x3C, opc2 | 2, opc3, 0, PPC_NONE, fl2), \
GEN_HANDLER2_E(name, #name, 0x3C, opc2 | 3, opc3, 0, PPC_NONE, fl2)

#define GEN_XX3FORM_NAME(name, opcname, opc2, opc3, fl2)               \
GEN_HANDLER2_E(name, opcname, 0x3C, opc2 | 0, opc3, 0, PPC_NONE, fl2), \
GEN_HANDLER2_E(name, opcname, 0x3C, opc2 | 1, opc3, 0, PPC_NONE, fl2), \
GEN_HANDLER2_E(name, opcname, 0x3C, opc2 | 2, opc3, 0, PPC_NONE, fl2), \
GEN_HANDLER2_E(name, opcname, 0x3C, opc2 | 3, opc3, 0, PPC_NONE, fl2)

#define GEN_XX2IFORM(name, opc2, opc3, fl2)                           \
GEN_HANDLER2_E(name, #name, 0x3C, opc2 | 0, opc3, 1, PPC_NONE, fl2), \
GEN_HANDLER2_E(name, #name, 0x3C, opc2 | 1, opc3, 1, PPC_NONE, fl2), \
GEN_HANDLER2_E(name, #name, 0x3C, opc2 | 2, opc3, 1, PPC_NONE, fl2), \
GEN_HANDLER2_E(name, #name, 0x3C, opc2 | 3, opc3, 1, PPC_NONE, fl2)

#define GEN_XX3FORM_DM(name, opc2, opc3) \
GEN_HANDLER2_E(name, #name, 0x3C, opc2|0x00, opc3|0x00, 0, PPC_NONE, PPC2_VSX),\
GEN_HANDLER2_E(name, #name, 0x3C, opc2|0x01, opc3|0x00, 0, PPC_NONE, PPC2_VSX),\
GEN_HANDLER2_E(name, #name, 0x3C, opc2|0x02, opc3|0x00, 0, PPC_NONE, PPC2_VSX),\
GEN_HANDLER2_E(name, #name, 0x3C, opc2|0x03, opc3|0x00, 0, PPC_NONE, PPC2_VSX),\
GEN_HANDLER2_E(name, #name, 0x3C, opc2|0x00, opc3|0x04, 0, PPC_NONE, PPC2_VSX),\
GEN_HANDLER2_E(name, #name, 0x3C, opc2|0x01, opc3|0x04, 0, PPC_NONE, PPC2_VSX),\
GEN_HANDLER2_E(name, #name, 0x3C, opc2|0x02, opc3|0x04, 0, PPC_NONE, PPC2_VSX),\
GEN_HANDLER2_E(name, #name, 0x3C, opc2|0x03, opc3|0x04, 0, PPC_NONE, PPC2_VSX),\
GEN_HANDLER2_E(name, #name, 0x3C, opc2|0x00, opc3|0x08, 0, PPC_NONE, PPC2_VSX),\
GEN_HANDLER2_E(name, #name, 0x3C, opc2|0x01, opc3|0x08, 0, PPC_NONE, PPC2_VSX),\
GEN_HANDLER2_E(name, #name, 0x3C, opc2|0x02, opc3|0x08, 0, PPC_NONE, PPC2_VSX),\
GEN_HANDLER2_E(name, #name, 0x3C, opc2|0x03, opc3|0x08, 0, PPC_NONE, PPC2_VSX),\
GEN_HANDLER2_E(name, #name, 0x3C, opc2|0x00, opc3|0x0C, 0, PPC_NONE, PPC2_VSX),\
GEN_HANDLER2_E(name, #name, 0x3C, opc2|0x01, opc3|0x0C, 0, PPC_NONE, PPC2_VSX),\
GEN_HANDLER2_E(name, #name, 0x3C, opc2|0x02, opc3|0x0C, 0, PPC_NONE, PPC2_VSX),\
GEN_HANDLER2_E(name, #name, 0x3C, opc2|0x03, opc3|0x0C, 0, PPC_NONE, PPC2_VSX)

#define GEN_VSX_XFORM_300(name, opc2, opc3, inval) \
GEN_HANDLER_E(name, 0x3F, opc2, opc3, inval, PPC_NONE, PPC2_ISA300)

#define GEN_VSX_XFORM_300_EO(name, opc2, opc3, opc4, inval)             \
GEN_HANDLER_E_2(name, 0x3F, opc2, opc3, opc4, inval, PPC_NONE, PPC2_ISA300)

#define GEN_VSX_Z23FORM_300(name, opc2, opc3, opc4, inval) \
GEN_VSX_XFORM_300_EO(name, opc2, opc3 | 0x00, opc4 | 0x0, inval), \
GEN_VSX_XFORM_300_EO(name, opc2, opc3 | 0x08, opc4 | 0x0, inval), \
GEN_VSX_XFORM_300_EO(name, opc2, opc3 | 0x10, opc4 | 0x0, inval), \
GEN_VSX_XFORM_300_EO(name, opc2, opc3 | 0x18, opc4 | 0x0, inval), \
GEN_VSX_XFORM_300_EO(name, opc2, opc3 | 0x00, opc4 | 0x1, inval), \
GEN_VSX_XFORM_300_EO(name, opc2, opc3 | 0x08, opc4 | 0x1, inval), \
GEN_VSX_XFORM_300_EO(name, opc2, opc3 | 0x10, opc4 | 0x1, inval), \
GEN_VSX_XFORM_300_EO(name, opc2, opc3 | 0x18, opc4 | 0x1, inval)

GEN_VSX_Z23FORM_300(xsrqpi, 0x05, 0x0, 0x0, 0x0),
GEN_VSX_Z23FORM_300(xsrqpxp, 0x05, 0x1, 0x0, 0x0),
GEN_VSX_XFORM_300_EO(xssqrtqp, 0x04, 0x19, 0x1B, 0x0),
GEN_VSX_XFORM_300(xssubqp, 0x04, 0x10, 0x0),

GEN_XX2FORM(xsabsdp, 0x12, 0x15, PPC2_VSX),
GEN_XX2FORM(xsnabsdp, 0x12, 0x16, PPC2_VSX),
GEN_XX2FORM(xsnegdp, 0x12, 0x17, PPC2_VSX),
GEN_XX3FORM(xscpsgndp, 0x00, 0x16, PPC2_VSX),

GEN_VSX_XFORM_300_EO(xsabsqp, 0x04, 0x19, 0x00, 0x00000001),
GEN_VSX_XFORM_300_EO(xsnabsqp, 0x04, 0x19, 0x08, 0x00000001),
GEN_VSX_XFORM_300_EO(xsnegqp, 0x04, 0x19, 0x10, 0x00000001),
GEN_VSX_XFORM_300(xscpsgnqp, 0x04, 0x03, 0x00000001),
GEN_VSX_XFORM_300_EO(xscvdpqp, 0x04, 0x1A, 0x16, 0x00000001),
GEN_VSX_XFORM_300_EO(xscvqpsdz, 0x04, 0x1A, 0x19, 0x00000001),
GEN_VSX_XFORM_300_EO(xscvqpswz, 0x04, 0x1A, 0x09, 0x00000001),
GEN_VSX_XFORM_300_EO(xscvqpudz, 0x04, 0x1A, 0x11, 0x00000001),
GEN_VSX_XFORM_300_EO(xscvqpuwz, 0x04, 0x1A, 0x01, 0x00000001),

#ifdef TARGET_PPC64
GEN_XX2FORM_EO(xsxexpdp, 0x16, 0x15, 0x00, PPC2_ISA300),
GEN_VSX_XFORM_300_EO(xsxexpqp, 0x04, 0x19, 0x02, 0x00000001),
GEN_XX2FORM_EO(xsxsigdp, 0x16, 0x15, 0x01, PPC2_ISA300),
GEN_VSX_XFORM_300_EO(xsxsigqp, 0x04, 0x19, 0x12, 0x00000001),
GEN_HANDLER_E(xsiexpdp, 0x3C, 0x16, 0x1C, 0, PPC_NONE, PPC2_ISA300),
GEN_VSX_XFORM_300(xsiexpqp, 0x4, 0x1B, 0x00000001),
#endif

GEN_XX3FORM(xviexpsp, 0x00, 0x1B, PPC2_ISA300),
GEN_XX3FORM(xviexpdp, 0x00, 0x1F, PPC2_ISA300),
GEN_XX2FORM_EO(xvxexpdp, 0x16, 0x1D, 0x00, PPC2_ISA300),
GEN_XX2FORM_EO(xvxsigdp, 0x16, 0x1D, 0x01, PPC2_ISA300),
GEN_XX2FORM_EO(xvxexpsp, 0x16, 0x1D, 0x08, PPC2_ISA300),

GEN_VSX_XFORM_300(xsaddqp, 0x04, 0x00, 0x0),
GEN_VSX_XFORM_300(xsmulqp, 0x04, 0x01, 0x0),
GEN_XX2FORM(xsredp,  0x14, 0x05, PPC2_VSX),
GEN_XX2FORM(xssqrtdp,  0x16, 0x04, PPC2_VSX),
GEN_XX2FORM(xsrsqrtedp,  0x14, 0x04, PPC2_VSX),
GEN_XX3FORM(xstdivdp,  0x14, 0x07, PPC2_VSX),
GEN_XX2FORM(xstsqrtdp,  0x14, 0x06, PPC2_VSX),
GEN_XX3FORM(xscmpexpdp, 0x0C, 0x07, PPC2_ISA300),
GEN_VSX_XFORM_300(xscmpexpqp, 0x04, 0x05, 0x00600001),
GEN_XX2IFORM(xscmpodp,  0x0C, 0x05, PPC2_VSX),
GEN_XX2IFORM(xscmpudp,  0x0C, 0x04, PPC2_VSX),
GEN_VSX_XFORM_300(xscmpoqp, 0x04, 0x04, 0x00600001),
GEN_VSX_XFORM_300(xscmpuqp, 0x04, 0x14, 0x00600001),
GEN_XX2FORM_EO(xscvdphp, 0x16, 0x15, 0x11, PPC2_ISA300),
GEN_XX2FORM(xscvdpsp, 0x12, 0x10, PPC2_VSX),
GEN_XX2FORM(xscvdpspn, 0x16, 0x10, PPC2_VSX207),
GEN_XX2FORM_EO(xscvhpdp, 0x16, 0x15, 0x10, PPC2_ISA300),
GEN_VSX_XFORM_300_EO(xscvsdqp, 0x04, 0x1A, 0x0A, 0x00000001),
GEN_XX2FORM(xscvspdp, 0x12, 0x14, PPC2_VSX),
GEN_XX2FORM(xscvdpsxds, 0x10, 0x15, PPC2_VSX),
GEN_XX2FORM(xscvdpsxws, 0x10, 0x05, PPC2_VSX),
GEN_XX2FORM(xscvdpuxds, 0x10, 0x14, PPC2_VSX),
GEN_XX2FORM(xscvdpuxws, 0x10, 0x04, PPC2_VSX),
GEN_XX2FORM(xscvsxddp, 0x10, 0x17, PPC2_VSX),
GEN_VSX_XFORM_300_EO(xscvudqp, 0x04, 0x1A, 0x02, 0x00000001),
GEN_XX2FORM(xscvuxddp, 0x10, 0x16, PPC2_VSX),
GEN_XX2FORM(xsrdpi, 0x12, 0x04, PPC2_VSX),
GEN_XX2FORM(xsrdpic, 0x16, 0x06, PPC2_VSX),
GEN_XX2FORM(xsrdpim, 0x12, 0x07, PPC2_VSX),
GEN_XX2FORM(xsrdpip, 0x12, 0x06, PPC2_VSX),
GEN_XX2FORM(xsrdpiz, 0x12, 0x05, PPC2_VSX),

GEN_VSX_XFORM_300(xsdivqp, 0x04, 0x11, 0x0),
GEN_XX2FORM(xsresp,  0x14, 0x01, PPC2_VSX207),
GEN_XX2FORM(xsrsp, 0x12, 0x11, PPC2_VSX207),
GEN_XX2FORM(xssqrtsp,  0x16, 0x00, PPC2_VSX207),
GEN_XX2FORM(xsrsqrtesp,  0x14, 0x00, PPC2_VSX207),
GEN_XX2FORM(xscvsxdsp, 0x10, 0x13, PPC2_VSX207),
GEN_XX2FORM(xscvuxdsp, 0x10, 0x12, PPC2_VSX207),

GEN_XX2FORM(xvredp,  0x14, 0x0D, PPC2_VSX),
GEN_XX2FORM(xvsqrtdp,  0x16, 0x0C, PPC2_VSX),
GEN_XX2FORM(xvrsqrtedp,  0x14, 0x0C, PPC2_VSX),
GEN_XX3FORM(xvtdivdp, 0x14, 0x0F, PPC2_VSX),
GEN_XX2FORM(xvtsqrtdp, 0x14, 0x0E, PPC2_VSX),
GEN_XX3FORM_NAME(xvmadddp, "xvmaddadp", 0x04, 0x0C, PPC2_VSX),
GEN_XX3FORM_NAME(xvmadddp, "xvmaddmdp", 0x04, 0x0D, PPC2_VSX),
GEN_XX3FORM_NAME(xvmsubdp, "xvmsubadp", 0x04, 0x0E, PPC2_VSX),
GEN_XX3FORM_NAME(xvmsubdp, "xvmsubmdp", 0x04, 0x0F, PPC2_VSX),
GEN_XX3FORM_NAME(xvnmadddp, "xvnmaddadp", 0x04, 0x1C, PPC2_VSX),
GEN_XX3FORM_NAME(xvnmadddp, "xvnmaddmdp", 0x04, 0x1D, PPC2_VSX),
GEN_XX3FORM_NAME(xvnmsubdp, "xvnmsubadp", 0x04, 0x1E, PPC2_VSX),
GEN_XX3FORM_NAME(xvnmsubdp, "xvnmsubmdp", 0x04, 0x1F, PPC2_VSX),
GEN_XX2FORM(xvcvdpsp, 0x12, 0x18, PPC2_VSX),
GEN_XX2FORM(xvcvdpsxds, 0x10, 0x1D, PPC2_VSX),
GEN_XX2FORM(xvcvdpsxws, 0x10, 0x0D, PPC2_VSX),
GEN_XX2FORM(xvcvdpuxds, 0x10, 0x1C, PPC2_VSX),
GEN_XX2FORM(xvcvdpuxws, 0x10, 0x0C, PPC2_VSX),
GEN_XX2FORM(xvcvsxddp, 0x10, 0x1F, PPC2_VSX),
GEN_XX2FORM(xvcvuxddp, 0x10, 0x1E, PPC2_VSX),
GEN_XX2FORM(xvcvsxwdp, 0x10, 0x0F, PPC2_VSX),
GEN_XX2FORM(xvcvuxwdp, 0x10, 0x0E, PPC2_VSX),
GEN_XX2FORM(xvrdpi, 0x12, 0x0C, PPC2_VSX),
GEN_XX2FORM(xvrdpic, 0x16, 0x0E, PPC2_VSX),
GEN_XX2FORM(xvrdpim, 0x12, 0x0F, PPC2_VSX),
GEN_XX2FORM(xvrdpip, 0x12, 0x0E, PPC2_VSX),
GEN_XX2FORM(xvrdpiz, 0x12, 0x0D, PPC2_VSX),

GEN_XX2FORM(xvresp, 0x14, 0x09, PPC2_VSX),
GEN_XX2FORM(xvsqrtsp, 0x16, 0x08, PPC2_VSX),
GEN_XX2FORM(xvrsqrtesp, 0x14, 0x08, PPC2_VSX),
GEN_XX3FORM(xvtdivsp, 0x14, 0x0B, PPC2_VSX),
GEN_XX2FORM(xvtsqrtsp, 0x14, 0x0A, PPC2_VSX),
GEN_XX3FORM_NAME(xvmaddsp, "xvmaddasp", 0x04, 0x08, PPC2_VSX),
GEN_XX3FORM_NAME(xvmaddsp, "xvmaddmsp", 0x04, 0x09, PPC2_VSX),
GEN_XX3FORM_NAME(xvmsubsp, "xvmsubasp", 0x04, 0x0A, PPC2_VSX),
GEN_XX3FORM_NAME(xvmsubsp, "xvmsubmsp", 0x04, 0x0B, PPC2_VSX),
GEN_XX3FORM_NAME(xvnmaddsp, "xvnmaddasp", 0x04, 0x18, PPC2_VSX),
GEN_XX3FORM_NAME(xvnmaddsp, "xvnmaddmsp", 0x04, 0x19, PPC2_VSX),
GEN_XX3FORM_NAME(xvnmsubsp, "xvnmsubasp", 0x04, 0x1A, PPC2_VSX),
GEN_XX3FORM_NAME(xvnmsubsp, "xvnmsubmsp", 0x04, 0x1B, PPC2_VSX),
GEN_XX2FORM(xvcvspdp, 0x12, 0x1C, PPC2_VSX),
GEN_XX2FORM(xvcvspsxds, 0x10, 0x19, PPC2_VSX),
GEN_XX2FORM(xvcvspsxws, 0x10, 0x09, PPC2_VSX),
GEN_XX2FORM(xvcvspuxds, 0x10, 0x18, PPC2_VSX),
GEN_XX2FORM(xvcvspuxws, 0x10, 0x08, PPC2_VSX),
GEN_XX2FORM(xvcvsxdsp, 0x10, 0x1B, PPC2_VSX),
GEN_XX2FORM(xvcvuxdsp, 0x10, 0x1A, PPC2_VSX),
GEN_XX2FORM(xvcvsxwsp, 0x10, 0x0B, PPC2_VSX),
GEN_XX2FORM(xvcvuxwsp, 0x10, 0x0A, PPC2_VSX),
GEN_XX2FORM(xvrspi, 0x12, 0x08, PPC2_VSX),
GEN_XX2FORM(xvrspic, 0x16, 0x0A, PPC2_VSX),
GEN_XX2FORM(xvrspim, 0x12, 0x0B, PPC2_VSX),
GEN_XX2FORM(xvrspip, 0x12, 0x0A, PPC2_VSX),
GEN_XX2FORM(xvrspiz, 0x12, 0x09, PPC2_VSX),
GEN_XX2FORM_EO(xxbrh, 0x16, 0x1D, 0x07, PPC2_ISA300),
GEN_XX2FORM_EO(xxbrw, 0x16, 0x1D, 0x0F, PPC2_ISA300),
GEN_XX2FORM_EO(xxbrd, 0x16, 0x1D, 0x17, PPC2_ISA300),
GEN_XX2FORM_EO(xvcvhpsp, 0x16, 0x1D, 0x18, PPC2_ISA300),
GEN_XX2FORM_EO(xvcvsphp, 0x16, 0x1D, 0x19, PPC2_ISA300),
GEN_XX2FORM_EO(xxbrq, 0x16, 0x1D, 0x1F, PPC2_ISA300),

GEN_XX3FORM(xxmrghw, 0x08, 0x02, PPC2_VSX),
GEN_XX3FORM(xxmrglw, 0x08, 0x06, PPC2_VSX),
GEN_XX3FORM_DM(xxsldwi, 0x08, 0x00),
