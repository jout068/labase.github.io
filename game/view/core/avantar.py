#! /usr/bin/env python
# -*- coding: UTF8 -*-
"""Controls UI page and responds to actions.

.. codeauthor:: Carlo Oliveira <carlo@nce.ufrj.br>

Changelog
---------
.. versionadded::    23.09
        Support the creation of a new level panel (28).
        Refactor for small data entry, new card and modal (22).
        Registra os três níveis e inicia o datasource (21a).
        Gerencia a mudança de nível no cliente (21).
        Create new project, package and module (17).

|   **Open Source Notification:** This file is part of open source program **Alite**
|   **Copyright © 2023  Carlo Oliveira** <carlo@nce.ufrj.br>,
|   **SPDX-License-Identifier:** `GNU General Public License v3.0 or later <https://is.gd/3Udt>`_.
|   `Labase <http://labase.selfip.org/>`_ - `NCE <https://portal.nce.ufrj.br>`_ - `UFRJ <https://ufrj.br/>`_.
"""
import uuid
from collections import namedtuple

ELEM_ID = "opn eng dis clo exi mod name_ desc_".split()
Level = namedtuple("Level", "descript name title extra")
ObjectId = namedtuple("ObjectId", "opn eng dis clo exi mod name_ desc_")
OI = ObjectId(**{suf: str(suf if "_" in suf else f"_modal_{suf}") for suf in ELEM_ID})


class DATA:
    TEX0 = dict(descript="Create a new Python project - New Project - Click Here",
                name="Novo Projeto - Clique Aqui",
                title="Novo Projeto",
                extra="../image/montroig.jpg"
                )
    MOD0 = dict(descript="Defina seu novo Projeto",
                name="Novo Projeto - Clique Aqui",
                title="Descreva seu Novo Pacote",
                extra=("O nome do pacote com uma única palavra minúscula e sem acentos.",
                       "Um texto de uma linha descrevendo o pacote."),
                )
    TEX1 = dict(descript="Create a new Python packet - New Packet - Click Here",
                name="Novo Pacote - Clique Aqui",
                title="Novo Pacote",
                extra="../image/garden.jpg"
                )
    MOD1 = dict(descript="Defina seu novo pacote",
                name="Novo Pacote - Clique Aqui",
                title="Descreva seu Novo Pacote",
                extra=("O nome do pacote com uma única palavra minúscula e sem acentos.",
                       "Um texto de uma linha descrevendo o pacote."),
                )
    TEX2 = dict(descript="Create a new Python Module - New Module - Click Here",
                name="Novo Módulo - Clique Aqui",
                title="Novo Módulo",
                extra="../image/montroig.jpg"
                )
    MOD2 = dict(descript="Defina seu novo Módulo",
                name="Novo Módulo - Clique Aqui",
                title="Descreva seu Novo Módulo",
                extra=("O nome do Módulo com uma única palavra minúscula e sem acentos.",
                       "Um texto de uma linha descrevendo o Módulo."),
                )


LEVEL = dict(projeto=Level(**{s: str(t) for s, t in DATA.TEX0.items()}),
             projeto_modal=Level(**{s: str(t) for s, t in DATA.MOD0.items()}),
             pacote=Level(**{s: str(t) for s, t in DATA.TEX1.items()}),
             pacote_modal=Level(**{s: str(t) for s, t in DATA.MOD1.items()}),
             modulo=Level(**{s: str(t) for s, t in DATA.TEX2.items()}),
             modulo_modal=Level(**{s: str(t) for s, t in DATA.MOD2.items()}))
LEVELS = "projeto pacote modulo".split()


class DataSource:
    def __init__(self):
        # @dataclass
        class LevelData:
            descript: str
            name: str
            title: str
            extra: str
            pad: str

            def __init__(self, descript: str, name: str, title: str, extra: str, pad: str):
                self.descript, self.name, self.title, self.extra = descript, name, title, extra
                self.pad = pad

            def as_dictionary(self):
                return {k: getattr(self, k) for k in "descript, name, title, extra".split(", ")}

            def as_dict(self):
                return {k: str(v) for k, v in self.as_dictionary().items()}

        # @dataclass
        class LevelContent:
            pid: str
            pad: list

            def __init__(self, pid, pad):
                self.pid, self.pad = pid, pad

            def as_dictionary(self):
                return {k: getattr(self, k) for k in "pid pad".split()}

            def as_dict(self):
                return {k: str(v) for k, v in self.as_dictionary().items()}

            def upsert(self, _pad):
                data = _pad if isinstance(_pad, list) else [_pad]
                self.pad = self.pad + data if self.pad else data

        self.data_buffer = {}
        self.level = LevelData
        self.content = LevelContent

    def save_cnt(self, pid, pad):
        # print("save_cnt(self, pid, pad)", pid, pad, self.data_buffer[pid])
        data = self.data_buffer[pid].pad if pid in self.data_buffer else []
        _ = data.extend(pad) if isinstance(pad, list) else data.append(pad)
        if pid in self.data_buffer:
            self.data_buffer[pid].upsert(data)
        else:
            self.data_buffer[pid] = self.content(pid, data)

    def load_cnt(self, pid):
        data = self.data_buffer[pid].pad
        print("load_cnt", pid, data)
        data = [self.data_buffer[pd] for pd in data if pd in self.data_buffer]

        return data

    def save(self, descript, name, title, extra, pad=None):
        import json
        pad = pad or str(uuid.uuid4().fields[-1])[:9]
        data = self.level(descript, name, title, extra, pad).as_dict()
        self.data_buffer[pad] = json.dumps(data)
        return data

    def load(self, pad):
        import json
        data = json.loads(self.data_buffer[pad])
        data = self.level(**data)
        return data.as_dict()


class Html:
    def __init__(self, html):
        self.tags = html.DIV, html.FIGURE, html.A, html.IMG, html.SPAN, html.H4, html.H1
        self.tagr = (html.P, html.BUTTON, html.HEADER, html.SECTION, html.FORM,
                     html.FIELDSET, html.INPUT, html.LEGEND, html.LABEL, html.FOOTER)
        self.tags_one = "d, f, a, i, s, h, h1".split(", ")
        self.tags_two = "p, b, hd, sc, fm, fs, ip, lg, lb, ft".split(", ")
        [setattr(self, name, value) for name, value in zip(self.tags_one, self.tags)]
        [setattr(self, name, value) for name, value in zip(self.tags_two, self.tagr)]

    def get_one(self):
        return [getattr(self, name) for name in self.tags_one]

    def get_two(self):
        return [getattr(self, name) for name in self.tags_two]


class Action:

    def __init__(self, document, html):
        self.document = document
        level_state = zip("projeto pacote modulo".split(), "pacote modulo projeto".split())
        self.current_level = "projeto"
        self.level = {lvl: nxt for lvl, nxt in level_state}
        self.content = {k: 0 for k in self.level.keys()}
        self.modal_id = [suf for suf in ELEM_ID]
        self.h_one = Html(html)
        self.modal = {}
        self.data = DataSource()
        self.bnd = [self.open_modal, self.execute_modal] + [self.close_modal] * 3
        self.levels = self.populate()

    def populate(self):
        _ = self.data.save(**LEVEL["projeto"]._asdict(), pad="__projeto@__")
        _ = self.data.save(**LEVEL["pacote"]._asdict(), pad="__pacote@__")
        _ = self.data.save(**LEVEL["modulo"]._asdict(), pad="__modulo@__")
        lvs = dict(__projeto__="__projeto@__", __pacote__="__pacote@__", __modulo__="__modulo@__")
        [self.data.save_cnt(pid, pad) for pid, pad in lvs.items()]
        return lvs

    def build(self):
        self.document["_panel"].html = ""
        current_level_text = LEVEL[self.current_level]
        current_level_modal = LEVEL[f"{self.current_level}_modal"]
        _ = self.document["_panel"] <= self.create_card(current_level_text)
        self.document["_modal_mod"].remove()
        _ = self.document.body <= self.create_modal(current_level_text, current_level_modal)
        self.modal = {inx: self.document[tg] for inx, tg in OI._asdict().items()}
        [self.modal[bid].bind("click", handler) for bid, handler in zip(self.modal_id, self.bnd)]

    def open_modal(self, ev):
        ev.stopPropagation()
        ev.preventDefault()
        print("open")
        self.modal["mod"].classList.add('is-active')

    def close_modal(self, ev):
        ev.stopPropagation()
        ev.preventDefault()
        self.modal["mod"].classList.remove('is-active')

    def execute_modal(self, ev):
        ev.stopPropagation()
        ev.preventDefault()
        name, desc = self.modal["name_"].value, self.modal["desc_"].value,
        self.modal["mod"].classList.remove('is-active')
        extra = LEVEL[self.current_level].extra
        inst = f"Entre no Projeto {name.capitalize()} -Clique Aqui"
        level_off = self.content[self.current_level]
        top, left = (level_off // 4) * -100, (level_off % 4) * -100
        print(level_off, top, left)
        s = f"opacity:0.7; position: absolute; min-width: 400%; min-height: 400%; top:{top}%; left:{left}%;"
        _panel_text = Level(desc, f"Projeto {name.capitalize()}", name, extra)
        _binder = lambda *_: self.create_panel(_panel_text)
        texto = Level(desc, inst, f"Projeto {name.capitalize()}", extra)
        self.content[self.current_level] += 1
        _ = self.document["_panel"] <= self.create_card(texto, s, f"_prj_{name}_", _binder=_binder)

    def create_panel(self, v):
        self.current_level = self.level[self.current_level]
        _ = self.document["_panel_title"].html = v.name
        _ = self.document["_panel_subtitle"].html = v.descript
        _ = self.document["_panel"].html = ""
        s = "opacity:0.5; filter:brightness(200%) blur(4px)"
        lev = self.current_level.capitalize()
        dsl = f"Create a new Python {lev} - New {lev} - Click Here"
        lvd = LEVEL[self.current_level].extra
        _create_button = Level(dsl, f"Novo {lev} - Clique Aqui", f"Novo {lev}", lvd)
        _binder, bnd = self.open_modal, f"_prj_{self.current_level}_"
        _ = self.document["_panel"] <= self.create_card(_create_button, s, bind_id=bnd, _binder=_binder)

    def create_card(self, v, style=None, bind_id=None, _binder=None):
        d, f, a, i, s, h, _ = self.h_one.get_one()
        o = bind_id or OI.opn
        h_tit, title, name, descript = v.extra, v.title, v.name, v.descript
        style = style or "opacity:0.5; filter:brightness(200%) blur(1px)"
        card = d(
            hdl := d([d(f(a(i(src=h_tit, style=style)), Class="image is-4by3 is-clipped"), Class="card-image"),
                      d(s(title), Class="card-content is-overlay is-size-1 has-text-weight-bold has-text-black"),
                      d(h(name, Class="title is-4"), Class="card-content-header"),
                      s(descript)],  # , id=m1)
                     Class="card", style="height:100%; overflow:hidden", id=o), Class="column is-4")
        hdl.bind("click", _binder) if _binder else None
        return card

    def create_modal(self, tx, tm):
        def field(_name=ELEM_ID[-2], ph="nome_do_projeto", hlp=""):
            return d(lb(name, For=_name, Class="label") +
                     d(ip(id=_name, name=_name, type="text", placeholder=ph, Class="input") +
                       p(hlp, Class="help"), Class="control"))

        d, f, a, i, s, h, h1 = self.h_one.get_one()
        p, b, hd, sc, fm, fs, ip, lg, lb, ft = self.h_one.get_two()
        mod, opn, eng, dis, clo, exi = OI.mod, OI.opn, OI.eng, OI.dis, OI.clo, OI.exi
        descript = tm.title
        name = tx.name
        title = tx.title
        h_nam, h_dsc = tm.name, tm.descript
        ii, ig = "button is-info", "button is-danger"
        card = d(
            d(hd(p(descript, Class="modal-card-title") +
                 b(Class="delete", id=exi, ariaLabel="close"), Class="modal-card-head") +
              sc(d(fm(
                  fs(lg(title) + field(hlp=h_nam) + field(_name=ELEM_ID[-1], hlp=h_dsc, ph="descreve o projeto")),
                  Class="form-horizontal"), Class="content"), Class="modal-card-body") +
              ft(b("Enviar", Class=ii, id=eng) + b("Cancelar", Class=ii, id=dis) +
                 b("Fechar", Class=ig, id=clo), Class="modal-card-foot"), Class="modal-card"),
            Class="modal", id=mod)
        return card


def to_yaml():
    pass


if __name__ == '__main__':
    to_yaml()