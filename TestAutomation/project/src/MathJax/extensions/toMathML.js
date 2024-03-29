/*
 *  /MathJax/extensions/toMathML.js
 *
 *  Copyright (c) 2009-2015 The MathJax Consortium
 *
 *  Licensed under the Apache License, Version 2.0 (the "License");
 *  you may not use this file except in compliance with the License.
 *  You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 *  Unless required by applicable law or agreed to in writing, software
 *  distributed under the License is distributed on an "AS IS" BASIS,
 *  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 *  See the License for the specific language governing permissions and
 *  limitations under the License.
 */
MathJax.Hub.Register.LoadHook("[MathJax]/jax/element/mml/jax.js", function() {
    var b = "2.5.0";
    var a = MathJax.ElementJax.mml;
    SETTINGS = MathJax.Hub.config.menuSettings;
    a.mbase.Augment({
        toMathML: function(k) {
            var g = (this.inferred && this.parent.inferRow);
            if (k == null) {
                k = ""
            }
            var e = this.type,
                d = this.toMathMLattributes();
            if (e === "mspace") {
                return k + "<" + e + d + " />"
            }
            var j = [],
                h = (this.isToken ? "" : k + (g ? "" : "  "));
            for (var f = 0, c = this.data.length; f < c; f++) {
                if (this.data[f]) {
                    j.push(this.data[f].toMathML(h))
                } else {
                    if (!this.isToken && !this.isChars) {
                        j.push(h + "<mrow />")
                    }
                }
            }
            if (this.isToken || this.isChars) {
                return k + "<" + e + d + ">" + j.join("") + "</" + e + ">"
            }
            if (g) {
                return j.join("\n")
            }
            if (j.length === 0 || (j.length === 1 && j[0] === "")) {
                return k + "<" + e + d + " />"
            }
            return k + "<" + e + d + ">\n" + j.join("\n") + "\n" + k + "</" + e + ">"
        },
        toMathMLattributes: function() {
            var h = (this.type === "mstyle" ? a.math.prototype.defaults : this.defaults);
            var g = (this.attrNames || a.copyAttributeNames),
                f = a.skipAttributes,
                k = a.copyAttributes;
            var d = [];
            if (this.type === "math" && (!this.attr || !this.attr.xmlns)) {
                d.push('xmlns="http://www.w3.org/1998/Math/MathML"')
            }
            if (!this.attrNames) {
                for (var j in h) {
                    if (!f[j] && !k[j] && h.hasOwnProperty(j)) {
                        if (this[j] != null && this[j] !== h[j]) {
                            if (this.Get(j, null, 1) !== this[j]) {
                                d.push(j + '="' + this.toMathMLattribute(this[j]) + '"')
                            }
                        }
                    }
                }
            }
            for (var e = 0, c = g.length; e < c; e++) {
                if (k[g[e]] === 1 && !h.hasOwnProperty(g[e])) {
                    continue
                }
                value = (this.attr || {})[g[e]];
                if (value == null) {
                    value = this[g[e]]
                }
                if (value != null) {
                    d.push(g[e] + '="' + this.toMathMLquote(value) + '"')
                }
            }
            this.toMathMLclass(d);
            if (d.length) {
                return " " + d.join(" ")
            } else {
                return ""
            }
        },
        toMathMLclass: function(c) {
            var e = [];
            if (this["class"]) {
                e.push(this["class"])
            }
            if (this.isa(a.TeXAtom) && SETTINGS.texHints) {
                var d = ["ORD", "OP", "BIN", "REL", "OPEN", "CLOSE", "PUNCT", "INNER", "VCENTER"][this.texClass];
                if (d) {
                    e.push("MJX-TeXAtom-" + d)
                }
            }
            if (this.mathvariant && this.toMathMLvariants[this.mathvariant]) {
                e.push("MJX" + this.mathvariant)
            }
            if (this.variantForm) {
                e.push("MJX-variant")
            }
            if (e.length) {
                c.unshift('class="' + e.join(" ") + '"')
            }
        },
        toMathMLattribute: function(c) {
            if (typeof(c) === "string" && c.replace(/ /g, "").match(/^(([-+])?(\d+(\.\d*)?|\.\d+))mu$/)) {
                return (RegExp.$2 || "") + ((1 / 18) * RegExp.$3).toFixed(3).replace(/\.?0+$/, "") + "em"
            } else {
                if (this.toMathMLvariants[c]) {
                    return this.toMathMLvariants[c]
                }
            }
            return this.toMathMLquote(c)
        },
        toMathMLvariants: {
            "-tex-caligraphic": a.VARIANT.SCRIPT,
            "-tex-caligraphic-bold": a.VARIANT.BOLDSCRIPT,
            "-tex-oldstyle": a.VARIANT.NORMAL,
            "-tex-oldstyle-bold": a.VARIANT.BOLD,
            "-tex-mathit": a.VARIANT.ITALIC
        },
        toMathMLquote: function(f) {
            f = String(f).split("");
            for (var g = 0, d = f.length; g < d; g++) {
                var k = f[g].charCodeAt(0);
                if (k <= 55295 || 57344 <= k) {
                    if (k > 126 || (k < 32 && k !== 10 && k !== 13 && k !== 9)) {
                        f[g] = "&#x" + k.toString(16).toUpperCase() + ";"
                    } else {
                        var j = {
                            "&": "&amp;",
                            "<": "&lt;",
                            ">": "&gt;",
                            '"': "&quot;"
                        }[f[g]];
                        if (j) {
                            f[g] = j
                        }
                    }
                } else {
                    if (g + 1 < d) {
                        var h = f[g + 1].charCodeAt(0);
                        var e = (((k - 55296) << 10) + (h - 56320) + 65536);
                        f[g] = "&#x" + e.toString(16).toUpperCase() + ";";
                        f[g + 1] = "";
                        g++
                    } else {
                        f[g] = ""
                    }
                }
            }
            return f.join("")
        }
    });
    a.math.Augment({
        toMathML: function(c, d) {
            var f;
            if (c == null) {
                c = ""
            }
            if (d && d.originalText && SETTINGS.semantics) {
                f = MathJax.InputJax[d.inputJax].annotationEncoding
            }
            var l = (this.data[0] && this.data[0].data.length > 1);
            var o = this.type,
                j = this.toMathMLattributes();
            var h = [],
                n = c + (f ? "  " + (l ? "  " : "") : "") + "  ";
            for (var g = 0, e = this.data.length; g < e; g++) {
                if (this.data[g]) {
                    h.push(this.data[g].toMathML(n))
                } else {
                    h.push(n + "<mrow />")
                }
            }
            if (h.length === 0 || (h.length === 1 && h[0] === "")) {
                if (!f) {
                    return "<" + o + j + " />"
                }
                h.push(n + "<mrow />")
            }
            if (f) {
                if (l) {
                    h.unshift(c + "    <mrow>");
                    h.push(c + "    </mrow>")
                }
                h.unshift(c + "  <semantics>");
                var k = d.originalText.replace(/[&<>]/g, function(i) {
                    return {
                        ">": "&gt;",
                        "<": "&lt;",
                        "&": "&amp;"
                    }[i]
                });
                h.push(c + '    <annotation encoding="' + f + '">' + k + "</annotation>");
                h.push(c + "  </semantics>")
            }
            return c + "<" + o + j + ">\n" + h.join("\n") + "\n" + c + "</" + o + ">"
        }
    });
    a.msubsup.Augment({
        toMathML: function(h) {
            var e = this.type;
            if (this.data[this.sup] == null) {
                e = "msub"
            }
            if (this.data[this.sub] == null) {
                e = "msup"
            }
            var d = this.toMathMLattributes();
            delete this.data[0].inferred;
            var g = [];
            for (var f = 0, c = this.data.length; f < c; f++) {
                if (this.data[f]) {
                    g.push(this.data[f].toMathML(h + "  "))
                }
            }
            return h + "<" + e + d + ">\n" + g.join("\n") + "\n" + h + "</" + e + ">"
        }
    });
    a.munderover.Augment({
        toMathML: function(h) {
            var e = this.type;
            if (this.data[this.under] == null) {
                e = "mover"
            }
            if (this.data[this.over] == null) {
                e = "munder"
            }
            var d = this.toMathMLattributes();
            delete this.data[0].inferred;
            var g = [];
            for (var f = 0, c = this.data.length; f < c; f++) {
                if (this.data[f]) {
                    g.push(this.data[f].toMathML(h + "  "))
                }
            }
            return h + "<" + e + d + ">\n" + g.join("\n") + "\n" + h + "</" + e + ">"
        }
    });
    a.TeXAtom.Augment({
        toMathML: function(d) {
            var c = this.toMathMLattributes();
            if (!c && this.data[0].data.length === 1) {
                return d.substr(2) + this.data[0].toMathML(d)
            }
            return d + "<mrow" + c + ">\n" + this.data[0].toMathML(d + "  ") + "\n" + d + "</mrow>"
        }
    });
    a.chars.Augment({
        toMathML: function(c) {
            return (c || "") + this.toMathMLquote(this.toString())
        }
    });
    a.entity.Augment({
        toMathML: function(c) {
            return (c || "") + "&" + this.data[0] + ";<!-- " + this.toString() + " -->"
        }
    });
    a.xml.Augment({
        toMathML: function(c) {
            return (c || "") + this.toString()
        }
    });
    MathJax.Hub.Register.StartupHook("TeX mathchoice Ready", function() {
        a.TeXmathchoice.Augment({
            toMathML: function(c) {
                return this.Core().toMathML(c)
            }
        })
    });
    MathJax.Hub.Startup.signal.Post("toMathML Ready")
});
MathJax.Ajax.loadComplete("[MathJax]/extensions/toMathML.js");
