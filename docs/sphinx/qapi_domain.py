"""
QAPI domain extension.
"""

# The best laid plans of mice and men, ...
# pylint: disable=too-many-lines

from __future__ import annotations

from typing import (
    TYPE_CHECKING,
    AbstractSet,
    Any,
    Dict,
    Iterable,
    List,
    NamedTuple,
    Optional,
    Tuple,
    Union,
    cast,
)

from docutils import nodes
from docutils.parsers.rst import directives

from compat import (
    CompatField,
    CompatGroupedField,
    CompatTypedField,
    KeywordNode,
    ParserFix,
    Signature,
    SpaceNode,
)
from sphinx import addnodes
from sphinx.addnodes import desc_signature, pending_xref
from sphinx.directives import ObjectDescription
from sphinx.domains import (
    Domain,
    Index,
    IndexEntry,
    ObjType,
)
from sphinx.locale import _, __
from sphinx.roles import XRefRole
from sphinx.util import logging
from sphinx.util.nodes import make_id, make_refnode


if TYPE_CHECKING:
    from docutils.nodes import Element, Node

    from sphinx.application import Sphinx
    from sphinx.builders import Builder
    from sphinx.environment import BuildEnvironment
    from sphinx.util.typing import OptionSpec

logger = logging.getLogger(__name__)


def _unpack_field(
    field: nodes.Node,
) -> Tuple[nodes.field_name, nodes.field_body]:
    """
    docutils helper: unpack a field node in a type-safe manner.
    """
    assert isinstance(field, nodes.field)
    assert len(field.children) == 2
    assert isinstance(field.children[0], nodes.field_name)
    assert isinstance(field.children[1], nodes.field_body)
    return (field.children[0], field.children[1])


class ObjectEntry(NamedTuple):
    docname: str
    node_id: str
    objtype: str
    aliased: bool


class QAPIXRefRole(XRefRole):

    def process_link(
        self,
        env: BuildEnvironment,
        refnode: Element,
        has_explicit_title: bool,
        title: str,
        target: str,
    ) -> tuple[str, str]:
        refnode["qapi:module"] = env.ref_context.get("qapi:module")

        # Cross-references that begin with a tilde adjust the title to
        # only show the reference without a leading module, even if one
        # was provided. This is a Sphinx-standard syntax; give it
        # priority over QAPI-specific type markup below.
        hide_module = False
        if target.startswith("~"):
            hide_module = True
            target = target[1:]

        # Type names that end with "?" are considered optional
        # arguments and should be documented as such, but it's not
        # part of the xref itself.
        if target.endswith("?"):
            refnode["qapi:optional"] = True
            target = target[:-1]

        # Type names wrapped in brackets denote lists. strip the
        # brackets and remember to add them back later.
        if target.startswith("[") and target.endswith("]"):
            refnode["qapi:array"] = True
            target = target[1:-1]

        if has_explicit_title:
            # Don't mess with the title at all if it was explicitly set.
            # Explicit title syntax for references is e.g.
            # :qapi:type:`target <explicit title>`
            # and this explicit title overrides everything else here.
            return title, target

        title = target
        if hide_module:
            title = target.split(".")[-1]

        return title, target

    def result_nodes(
        self,
        document: nodes.document,
        env: BuildEnvironment,
        node: Element,
        is_ref: bool,
    ) -> Tuple[List[nodes.Node], List[nodes.system_message]]:

        # node here is the pending_xref node (or whatever nodeclass was
        # configured at XRefRole class instantiation time).
        results: List[nodes.Node] = [node]

        if node.get("qapi:array"):
            results.insert(0, nodes.literal("[", "["))
            results.append(nodes.literal("]", "]"))

        if node.get("qapi:optional"):
            results.append(nodes.Text(", "))
            results.append(nodes.emphasis("?", "optional"))

        return results, []


class QAPIDescription(ParserFix):
    """
    Generic QAPI description.

    This is meant to be an abstract class, not instantiated
    directly. This class handles the abstract details of indexing, the
    TOC, and reference targets for QAPI descriptions.
    """

    def handle_signature(self, sig: str, signode: desc_signature) -> Signature:
        # Do nothing. The return value here is the "name" of the entity
        # being documented; for QAPI, this is the same as the
        # "signature", which is just a name.

        # Normally this method must also populate signode with nodes to
        # render the signature; here we do nothing instead - the
        # subclasses will handle this.
        return sig

    def get_index_text(self, name: Signature) -> Tuple[str, str]:
        """Return the text for the index entry of the object."""

        # NB: this is used for the global index, not the QAPI index.
        return ("single", f"{name} (QMP {self.objtype})")

    def add_target_and_index(
        self, name: Signature, sig: str, signode: desc_signature
    ) -> None:
        # name is the return value of handle_signature.
        # sig is the original, raw text argument to handle_signature.
        # For QAPI, these are identical, currently.

        assert self.objtype

        # If we're documenting a module, don't include the module as
        # part of the FQN.
        modname = ""
        if self.objtype != "module":
            modname = self.options.get(
                "module", self.env.ref_context.get("qapi:module")
            )
        fullname = (modname + "." if modname else "") + name

        node_id = make_id(
            self.env, self.state.document, self.objtype, fullname
        )
        signode["ids"].append(node_id)

        self.state.document.note_explicit_target(signode)
        domain = cast(QAPIDomain, self.env.get_domain("qapi"))
        domain.note_object(fullname, self.objtype, node_id, location=signode)

        if "no-index-entry" not in self.options:
            arity, indextext = self.get_index_text(name)
            assert self.indexnode is not None
            if indextext:
                self.indexnode["entries"].append(
                    (arity, indextext, node_id, "", None)
                )

    def _object_hierarchy_parts(
        self, sig_node: desc_signature
    ) -> Tuple[str, ...]:
        if "fullname" not in sig_node:
            return ()
        modname = sig_node.get("module")
        fullname = sig_node["fullname"]

        if modname:
            return (modname, *fullname.split("."))

        return tuple(fullname.split("."))

    def _toc_entry_name(self, sig_node: desc_signature) -> str:
        # This controls the name in the TOC and on the sidebar.

        # This is the return type of _object_hierarchy_parts().
        toc_parts = cast(Tuple[str, ...], sig_node.get("_toc_parts", ()))
        if not toc_parts:
            return ""

        config = self.env.app.config
        *parents, name = toc_parts
        if config.toc_object_entries_show_parents == "domain":
            return sig_node.get("fullname", name)
        if config.toc_object_entries_show_parents == "hide":
            return name
        if config.toc_object_entries_show_parents == "all":
            return ".".join(parents + [name])
        return ""


class QAPIObject(QAPIDescription):
    """
    Description of a generic QAPI object.

    It's not used directly, but is instead subclassed by specific directives.
    """

    # Inherit some standard options from Sphinx's ObjectDescription
    option_spec: OptionSpec = (  # type:ignore[misc]
        ObjectDescription.option_spec.copy()
    )
    option_spec.update(
        {
            # Borrowed from the Python domain:
            "module": directives.unchanged,  # Override contextual module name
            # These are QAPI originals:
            "since": directives.unchanged,
            "ifcond": directives.unchanged,
            "deprecated": directives.flag,
            "unstable": directives.flag,
        }
    )

    doc_field_types = [
        # :feat name: descr
        CompatGroupedField(
            "feature",
            label=_("Features"),
            names=("feat",),
            can_collapse=False,
        ),
    ]

    def get_signature_prefix(self) -> List[nodes.Node]:
        """Return a prefix to put before the object name in the signature."""
        assert self.objtype
        return [
            KeywordNode("", self.objtype.title()),
            SpaceNode(" "),
        ]

    def get_signature_suffix(self) -> List[nodes.Node]:
        """Return a suffix to put after the object name in the signature."""
        ret: List[nodes.Node] = []

        if "since" in self.options:
            ret += [
                SpaceNode(" "),
                addnodes.desc_sig_element(
                    "", f"(Since: {self.options['since']})"
                ),
            ]

        return ret

    def handle_signature(self, sig: str, signode: desc_signature) -> Signature:
        """
        Transform a QAPI definition name into RST nodes.

        This method was originally intended for handling function
        signatures. In the QAPI domain, however, we only pass the
        definition name as the directive argument and handle everything
        else in the content body with field lists.

        As such, the only argument here is "sig", which is just the QAPI
        definition name.
        """
        modname = self.options.get(
            "module", self.env.ref_context.get("qapi:module")
        )

        signode["fullname"] = sig
        signode["module"] = modname
        sig_prefix = self.get_signature_prefix()
        if sig_prefix:
            signode += addnodes.desc_annotation(
                str(sig_prefix), "", *sig_prefix
            )
        signode += addnodes.desc_name(sig, sig)
        signode += self.get_signature_suffix()

        return sig

    def _add_infopips(self, contentnode: addnodes.desc_content) -> None:
        # Add various eye-catches and things that go below the signature
        # bar, but precede the user-defined content.
        infopips = nodes.container()
        infopips.attributes["classes"].append("qapi-infopips")

        def _add_pip(
            source: str, content: Union[str, List[nodes.Node]], classname: str
        ) -> None:
            node = nodes.container(source)
            if isinstance(content, str):
                node.append(nodes.Text(content))
            else:
                node.extend(content)
            node.attributes["classes"].extend(["qapi-infopip", classname])
            infopips.append(node)

        if "deprecated" in self.options:
            _add_pip(
                ":deprecated:",
                f"This {self.objtype} is deprecated.",
                "qapi-deprecated",
            )

        if "unstable" in self.options:
            _add_pip(
                ":unstable:",
                f"This {self.objtype} is unstable/experimental.",
                "qapi-unstable",
            )

        if self.options.get("ifcond", ""):
            ifcond = self.options["ifcond"]
            _add_pip(
                f":ifcond: {ifcond}",
                [
                    nodes.emphasis("", "Availability"),
                    nodes.Text(": "),
                    nodes.literal(ifcond, ifcond),
                ],
                "qapi-ifcond",
            )

        if infopips.children:
            contentnode.insert(0, infopips)

    def _validate_field(self, field: nodes.field) -> None:
        """Validate field lists in this QAPI Object Description."""
        name, _ = _unpack_field(field)
        allowed_fields = set(self.env.app.config.qapi_allowed_fields)

        field_label = name.astext()
        if field_label in allowed_fields:
            # Explicitly allowed field list name, OK.
            return

        try:
            # split into field type and argument (if provided)
            # e.g. `:arg type name: descr` is
            # field_type = "arg", field_arg = "type name".
            field_type, field_arg = field_label.split(None, 1)
        except ValueError:
            # No arguments provided
            field_type = field_label
            field_arg = ""

        typemap = self.get_field_type_map()
        if field_type in typemap:
            # This is a special docfield, yet-to-be-processed. Catch
            # correct names, but incorrect arguments. This mismatch WILL
            # cause Sphinx to render this field incorrectly (without a
            # warning), which is never what we want.
            typedesc = typemap[field_type][0]
            if typedesc.has_arg != bool(field_arg):
                msg = f"docfield field list type {field_type!r} "
                if typedesc.has_arg:
                    msg += "requires an argument."
                else:
                    msg += "takes no arguments."
                logger.warning(msg, location=field)
        else:
            # This is unrecognized entirely. It's valid rST to use
            # arbitrary fields, but let's ensure the documentation
            # writer has done this intentionally.
            valid = ", ".join(sorted(set(typemap) | allowed_fields))
            msg = (
                f"Unrecognized field list name {field_label!r}.\n"
                f"Valid fields for qapi:{self.objtype} are: {valid}\n"
                "\n"
                "If this usage is intentional, please add it to "
                "'qapi_allowed_fields' in docs/conf.py."
            )
            logger.warning(msg, location=field)

    def transform_content(self, content_node: addnodes.desc_content) -> None:
        # This hook runs after before_content and the nested parse, but
        # before the DocFieldTransformer is executed.
        super().transform_content(content_node)

        self._add_infopips(content_node)

        # Validate field lists.
        for child in content_node:
            if isinstance(child, nodes.field_list):
                for field in child.children:
                    assert isinstance(field, nodes.field)
                    self._validate_field(field)


class SpecialTypedField(CompatTypedField):
    def make_field(self, *args: Any, **kwargs: Any) -> nodes.field:
        ret = super().make_field(*args, **kwargs)

        # Look for the characteristic " -- " text node that Sphinx
        # inserts for each TypedField entry ...
        for node in ret.traverse(lambda n: str(n) == " -- "):
            par = node.parent
            if par.children[0].astext() != "q_dummy":
                continue

            # If the first node's text is q_dummy, this is a dummy
            # field we want to strip down to just its contents.
            del par.children[:-1]

        return ret


class QAPICommand(QAPIObject):
    """Description of a QAPI Command."""

    doc_field_types = QAPIObject.doc_field_types.copy()
    doc_field_types.extend(
        [
            # :arg TypeName ArgName: descr
            SpecialTypedField(
                "argument",
                label=_("Arguments"),
                names=("arg",),
                typerolename="type",
                can_collapse=False,
            ),
            # :error: descr
            CompatField(
                "error",
                label=_("Errors"),
                names=("error", "errors"),
                has_arg=False,
            ),
            # :return TypeName: descr
            CompatGroupedField(
                "returnvalue",
                label=_("Return"),
                rolename="type",
                names=("return",),
                can_collapse=True,
            ),
        ]
    )


class QAPIEnum(QAPIObject):
    """Description of a QAPI Enum."""

    doc_field_types = QAPIObject.doc_field_types.copy()
    doc_field_types.extend(
        [
            # :value name: descr
            CompatGroupedField(
                "value",
                label=_("Values"),
                names=("value",),
                can_collapse=False,
            )
        ]
    )


class QAPIAlternate(QAPIObject):
    """Description of a QAPI Alternate."""

    doc_field_types = QAPIObject.doc_field_types.copy()
    doc_field_types.extend(
        [
            # :alt type name: descr
            CompatTypedField(
                "alternative",
                label=_("Alternatives"),
                names=("alt",),
                typerolename="type",
                can_collapse=False,
            ),
        ]
    )


class QAPIObjectWithMembers(QAPIObject):
    """Base class for Events/Structs/Unions"""

    doc_field_types = QAPIObject.doc_field_types.copy()
    doc_field_types.extend(
        [
            # :member type name: descr
            SpecialTypedField(
                "member",
                label=_("Members"),
                names=("memb",),
                typerolename="type",
                can_collapse=False,
            ),
        ]
    )


class QAPIEvent(QAPIObjectWithMembers):
    # pylint: disable=too-many-ancestors
    """Description of a QAPI Event."""


class QAPIJSONObject(QAPIObjectWithMembers):
    # pylint: disable=too-many-ancestors
    """Description of a QAPI Object: structs and unions."""


class QAPIModule(QAPIDescription):
    """
    Directive to mark description of a new module.

    This directive doesn't generate any special formatting, and is just
    a pass-through for the content body. Named section titles are
    allowed in the content body.

    Use this directive to create entries for the QAPI module in the
    global index and the QAPI index; as well as to associate subsequent
    definitions with the module they are defined in for purposes of
    search and QAPI index organization.

    :arg: The name of the module.
    :opt no-index: Don't add cross-reference targets or index entries.
    :opt no-typesetting: Don't render the content body (but preserve any
       cross-reference target IDs in the squelched output.)

    Example::

       .. qapi:module:: block-core
          :no-index:
          :no-typesetting:

          Lorem ipsum, dolor sit amet ...
    """

    def run(self) -> List[Node]:
        modname = self.arguments[0].strip()
        self.env.ref_context["qapi:module"] = modname
        ret = super().run()

        # ObjectDescription always creates a visible signature bar. We
        # want module items to be "invisible", however.

        # Extract the content body of the directive:
        assert isinstance(ret[-1], addnodes.desc)
        desc_node = ret.pop(-1)
        assert isinstance(desc_node.children[1], addnodes.desc_content)
        ret.extend(desc_node.children[1].children)

        # Re-home node_ids so anchor refs still work:
        node_ids: List[str]
        if node_ids := [
            node_id
            for el in desc_node.children[0].traverse(nodes.Element)
            for node_id in cast(List[str], el.get("ids", ()))
        ]:
            target_node = nodes.target(ids=node_ids)
            ret.insert(1, target_node)

        return ret


class QAPIIndex(Index):
    """
    Index subclass to provide the QAPI definition index.
    """

    # pylint: disable=too-few-public-methods

    name = "index"
    localname = _("QAPI Index")
    shortname = _("QAPI Index")

    def generate(
        self,
        docnames: Optional[Iterable[str]] = None,
    ) -> Tuple[List[Tuple[str, List[IndexEntry]]], bool]:
        assert isinstance(self.domain, QAPIDomain)
        content: Dict[str, List[IndexEntry]] = {}
        collapse = False

        # list of all object (name, ObjectEntry) pairs, sorted by name
        # (ignoring the module)
        objects = sorted(
            self.domain.objects.items(),
            key=lambda x: x[0].split(".")[-1].lower(),
        )

        for objname, obj in objects:
            if docnames and obj.docname not in docnames:
                continue

            # Strip the module name out:
            objname = objname.split(".")[-1]

            # Add an alphabetical entry:
            entries = content.setdefault(objname[0].upper(), [])
            entries.append(
                IndexEntry(
                    objname, 0, obj.docname, obj.node_id, obj.objtype, "", ""
                )
            )

            # Add a categorical entry:
            category = obj.objtype.title() + "s"
            entries = content.setdefault(category, [])
            entries.append(
                IndexEntry(objname, 0, obj.docname, obj.node_id, "", "", "")
            )

        # alphabetically sort categories; type names first, ABC entries last.
        sorted_content = sorted(
            content.items(),
            key=lambda x: (len(x[0]) == 1, x[0]),
        )
        return sorted_content, collapse


class QAPIDomain(Domain):
    """QAPI language domain."""

    name = "qapi"
    label = "QAPI"

    # This table associates cross-reference object types (key) with an
    # ObjType instance, which defines the valid cross-reference roles
    # for each object type.
    #
    # e.g., the :qapi:type: cross-reference role can refer to enum,
    # struct, union, or alternate objects; but :qapi:obj: can refer to
    # anything. Each object also gets its own targeted cross-reference role.
    object_types: Dict[str, ObjType] = {
        "module": ObjType(_("module"), "mod", "any"),
        "command": ObjType(_("command"), "cmd", "any"),
        "event": ObjType(_("event"), "event", "any"),
        "enum": ObjType(_("enum"), "enum", "type", "any"),
        "object": ObjType(_("object"), "obj", "type", "any"),
        "alternate": ObjType(_("alternate"), "alt", "type", "any"),
    }

    # Each of these provides a rST directive,
    # e.g. .. qapi:module:: block-core
    directives = {
        "module": QAPIModule,
        "command": QAPICommand,
        "event": QAPIEvent,
        "enum": QAPIEnum,
        "object": QAPIJSONObject,
        "alternate": QAPIAlternate,
    }

    # These are all cross-reference roles; e.g.
    # :qapi:cmd:`query-block`. The keys correlate to the names used in
    # the object_types table values above.
    roles = {
        "mod": QAPIXRefRole(),
        "cmd": QAPIXRefRole(),
        "event": QAPIXRefRole(),
        "enum": QAPIXRefRole(),
        "obj": QAPIXRefRole(),  # specifically structs and unions.
        "alt": QAPIXRefRole(),
        # reference any data type (excludes modules, commands, events)
        "type": QAPIXRefRole(),
        "any": QAPIXRefRole(),  # reference *any* type of QAPI object.
    }

    # Moved into the data property at runtime;
    # this is the internal index of reference-able objects.
    initial_data: Dict[str, Dict[str, Tuple[Any]]] = {
        "objects": {},  # fullname -> ObjectEntry
    }

    # Index pages to generate; each entry is an Index class.
    indices = [
        QAPIIndex,
    ]

    @property
    def objects(self) -> Dict[str, ObjectEntry]:
        ret = self.data.setdefault("objects", {})
        return ret  # type: ignore[no-any-return]

    def note_object(
        self,
        name: str,
        objtype: str,
        node_id: str,
        aliased: bool = False,
        location: Any = None,
    ) -> None:
        """Note a QAPI object for cross reference."""
        if name in self.objects:
            other = self.objects[name]
            if other.aliased and aliased is False:
                # The original definition found. Override it!
                pass
            elif other.aliased is False and aliased:
                # The original definition is already registered.
                return
            else:
                # duplicated
                logger.warning(
                    __(
                        "duplicate object description of %s, "
                        "other instance in %s, use :no-index: for one of them"
                    ),
                    name,
                    other.docname,
                    location=location,
                )
        self.objects[name] = ObjectEntry(
            self.env.docname, node_id, objtype, aliased
        )

    def clear_doc(self, docname: str) -> None:
        for fullname, obj in list(self.objects.items()):
            if obj.docname == docname:
                del self.objects[fullname]

    def merge_domaindata(
        self, docnames: AbstractSet[str], otherdata: Dict[str, Any]
    ) -> None:
        for fullname, obj in otherdata["objects"].items():
            if obj.docname in docnames:
                # Sphinx's own python domain doesn't appear to bother to
                # check for collisions. Assert they don't happen and
                # we'll fix it if/when the case arises.
                assert fullname not in self.objects, (
                    "bug - collision on merge?"
                    f" {fullname=} {obj=} {self.objects[fullname]=}"
                )
                self.objects[fullname] = obj

    def find_obj(
        self, modname: str, name: str, typ: Optional[str]
    ) -> list[tuple[str, ObjectEntry]]:
        """
        Find a QAPI object for "name", perhaps using the given module.

        Returns a list of (name, object entry) tuples.

        :param modname: The current module context (if any!)
                        under which we are searching.
        :param name: The name of the x-ref to resolve;
                     may or may not include a leading module.
        :param type: The role name of the x-ref we're resolving, if provided.
                     (This is absent for "any" lookups.)
        """
        if not name:
            return []

        names: list[str] = []
        matches: list[tuple[str, ObjectEntry]] = []

        fullname = name
        if "." in fullname:
            # We're searching for a fully qualified reference;
            # ignore the contextual module.
            pass
        elif modname:
            # We're searching for something from somewhere;
            # try searching the current module first.
            # e.g. :qapi:cmd:`query-block` or `query-block` is being searched.
            fullname = f"{modname}.{name}"

        if typ is None:
            # type isn't specified, this is a generic xref.
            # search *all* qapi-specific object types.
            objtypes: List[str] = list(self.object_types)
        else:
            # type is specified and will be a role (e.g. obj, mod, cmd)
            # convert this to eligible object types (e.g. command, module)
            # using the QAPIDomain.object_types table.
            objtypes = self.objtypes_for_role(typ, [])

        if name in self.objects and self.objects[name].objtype in objtypes:
            names = [name]
        elif (
            fullname in self.objects
            and self.objects[fullname].objtype in objtypes
        ):
            names = [fullname]
        else:
            # exact match wasn't found; e.g. we are searching for
            # `query-block` from a different (or no) module.
            searchname = "." + name
            names = [
                oname
                for oname in self.objects
                if oname.endswith(searchname)
                and self.objects[oname].objtype in objtypes
            ]

        matches = [(oname, self.objects[oname]) for oname in names]
        if len(matches) > 1:
            matches = [m for m in matches if not m[1].aliased]
        return matches

    def resolve_xref(
        self,
        env: BuildEnvironment,
        fromdocname: str,
        builder: Builder,
        typ: str,
        target: str,
        node: pending_xref,
        contnode: Element,
    ) -> nodes.reference | None:
        modname = node.get("qapi:module")
        matches = self.find_obj(modname, target, typ)

        if not matches:
            # Normally, we could pass warn_dangling=True to QAPIXRefRole(),
            # but that will trigger on references to these built-in types,
            # which we'd like to ignore instead.

            # Take care of that warning here instead, so long as the
            # reference isn't to one of our built-in core types.
            if target not in (
                "string",
                "number",
                "int",
                "boolean",
                "null",
                "value",
                "q_empty",
            ):
                logger.warning(
                    __("qapi:%s reference target not found: %r"),
                    typ,
                    target,
                    type="ref",
                    subtype="qapi",
                    location=node,
                )
            return None

        if len(matches) > 1:
            logger.warning(
                __("more than one target found for cross-reference %r: %s"),
                target,
                ", ".join(match[0] for match in matches),
                type="ref",
                subtype="qapi",
                location=node,
            )

        name, obj = matches[0]
        return make_refnode(
            builder, fromdocname, obj.docname, obj.node_id, contnode, name
        )

    def resolve_any_xref(
        self,
        env: BuildEnvironment,
        fromdocname: str,
        builder: Builder,
        target: str,
        node: pending_xref,
        contnode: Element,
    ) -> List[Tuple[str, nodes.reference]]:
        results: List[Tuple[str, nodes.reference]] = []
        matches = self.find_obj(node.get("qapi:module"), target, None)
        for name, obj in matches:
            rolename = self.role_for_objtype(obj.objtype)
            assert rolename is not None
            role = f"qapi:{rolename}"
            refnode = make_refnode(
                builder, fromdocname, obj.docname, obj.node_id, contnode, name
            )
            results.append((role, refnode))
        return results


def setup(app: Sphinx) -> Dict[str, Any]:
    app.setup_extension("sphinx.directives")
    app.add_config_value(
        "qapi_allowed_fields",
        set(),
        "env",  # Setting impacts parsing phase
        types=set,
    )
    app.add_domain(QAPIDomain)

    return {
        "version": "1.0",
        "env_version": 1,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
