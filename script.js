
(function () {
  'use strict';
  document.body.classList.add('js');

  /* ── Langue ────────────────────────────────────────────────────────────
     Les deux langues sont dans le DOM, en attributs. Changer de langue
     reecrit du texte ; ca ne reconstruit pas la page et ca ne perd pas la
     position dans le defilement. */
  var LANGUE = 'fr';
  function langue(l) {
    LANGUE = l;
    document.documentElement.lang = l;
    var n = document.querySelectorAll('[data-fr]');
    for (var i = 0; i < n.length; i++) {
      var v = n[i].getAttribute('data-' + l);
      if (v === null) continue;
      /* textContent, jamais innerHTML : le contenu des attributs vient de
         contenu.py, mais l'ecrire en HTML ouvrirait la porte le jour ou il
         viendra d'ailleurs. */
      n[i].textContent = v;
    }
    var b = document.querySelectorAll('[data-langue]');
    for (var j = 0; j < b.length; j++) {
      b[j].setAttribute('aria-pressed',
        b[j].getAttribute('data-langue') === l ? 'true' : 'false');
    }
    try { localStorage.setItem('amaro-langue', l); } catch (e) {}
  }
  var lb = document.querySelectorAll('[data-langue]');
  for (var k = 0; k < lb.length; k++) {
    lb[k].addEventListener('click', function () {
      langue(this.getAttribute('data-langue'));
    });
  }
  try {
    var m = localStorage.getItem('amaro-langue');
    if (m === 'en') langue('en');
  } catch (e) {}

  /* ── Menu mobile ───────────────────────────────────────────────────── */
  var burger = document.getElementById('burger'),
      entete = document.getElementById('entete');
  if (burger && entete) {
    burger.addEventListener('click', function () {
      var o = entete.classList.toggle('ouvert');
      burger.setAttribute('aria-expanded', o ? 'true' : 'false');
    });
  }

  /* ── Apparitions ───────────────────────────────────────────────────── */
  var revs = document.querySelectorAll('.rev, [data-delai]');
  for (var r = 0; r < revs.length; r++) {
    if (!revs[r].classList.contains('rev')) revs[r].classList.add('rev');
    var d = revs[r].getAttribute('data-delai');
    if (d) revs[r].style.transitionDelay = d + 'ms';
  }
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (x) {
        if (x.isIntersecting) { x.target.classList.add('vu'); io.unobserve(x.target); }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.05 });
    for (var q = 0; q < revs.length; q++) io.observe(revs[q]);
  } else {
    /* Pas d'observateur : on montre tout. Un navigateur qui ne sait pas
       observer n'est pas un navigateur qui merite une page blanche. */
    for (var w = 0; w < revs.length; w++) revs[w].classList.add('vu');
  }

  /* ── Filtres du catalogue ──────────────────────────────────────────── */
  var filtres = document.getElementById('filtres');
  if (filtres) {
    var compte = document.getElementById('compte-produits');
    function filtrer() {
      var v = filtres.querySelector('input:checked');
      v = v ? v.value : 'tous';
      var p = document.querySelectorAll('#produits .produit'), n = 0;
      for (var i = 0; i < p.length; i++) {
        var ok = (v === 'tous' || p[i].getAttribute('data-cat') === v);
        p[i].hidden = !ok;
        if (ok) n++;
      }
      if (compte) {
        compte.textContent = n + (LANGUE === 'fr'
          ? (n > 1 ? ' produits' : ' produit')
          : (n > 1 ? ' products' : ' product'));
      }
    }
    filtres.addEventListener('change', filtrer);
    filtrer();
  }

  /* ── Formulaire B2B ────────────────────────────────────────────────── */
  var f = document.getElementById('b2b');
  if (f) {
    var MSG = {
      requis:   ['Ce champ est obligatoire.', 'This field is required.'],
      courriel: ['Adresse électronique invalide.', 'Invalid e-mail address.'],
      secteur:  ['Choisissez au moins un secteur.',
                 'Choose at least one sector.'],
      consent:  ['Votre accord est nécessaire pour traiter la demande.',
                 'Your agreement is required to handle the enquiry.']
    };
    function dire(cle) { return MSG[cle][LANGUE === 'en' ? 1 : 0]; }
    function erreur(nom, texte) {
      var p = document.getElementById('e-' + nom);
      if (p) p.textContent = texte || '';
      var bloc = f.querySelector('[data-champ="' + nom + '"]');
      if (bloc) bloc.classList.toggle('faux', !!texte);
    }
    f.addEventListener('submit', function (ev) {
      ev.preventDefault();
      var ok = true, premier = null;
      var champs = f.querySelectorAll('[data-champ]');
      for (var i = 0; i < champs.length; i++) {
        var nom = champs[i].getAttribute('data-champ');
        var ctrl = champs[i].querySelector('input,select,textarea');
        if (!ctrl) continue;
        var v = (ctrl.value || '').trim();
        if (ctrl.required && !v) {
          erreur(nom, dire('requis')); ok = false;
          if (!premier) premier = ctrl;
          continue;
        }
        if (ctrl.type === 'email' && v && !/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v)) {
          erreur(nom, dire('courriel')); ok = false;
          if (!premier) premier = ctrl;
          continue;
        }
        erreur(nom, '');
      }
      var sec = f.querySelectorAll('#secteurs input:checked');
      erreur('secteur', sec.length ? '' : dire('secteur'));
      if (!sec.length) { ok = false; if (!premier) premier = f.querySelector('#secteurs input'); }
      var cons = document.getElementById('f-consentement');
      erreur('consentement', cons && cons.checked ? '' : dire('consent'));
      if (cons && !cons.checked) { ok = false; if (!premier) premier = cons; }

      var res = document.getElementById('resultat');
      if (!ok) {
        if (res) res.hidden = true;
        if (premier) premier.focus();
        return;
      }
      if (f.getAttribute('action')) { f.submit(); return; }

      /* Pas d'action : on ne dit PAS « envoyé ». On montre ce qui partirait.
         Un accuse de reception sans destinataire est un mensonge poli, et
         c'est celui-la qu'un distributeur croit. */
      var lignes = [];
      var fd = new FormData(f);
      fd.forEach(function (val, cle) {
        if (String(val).trim()) lignes.push(cle + ' : ' + val);
      });
      if (res) {
        res.hidden = false;
        res.innerHTML = '';
        var box = document.createElement('div');
        box.className = 'avertissement';
        var t = document.createElement('p');
        t.innerHTML = '<strong>' + (LANGUE === 'en'
          ? 'Nothing was sent — and that is deliberate.'
          : 'Rien n’a été envoyé — et c’est volontaire.') + '</strong>';
        var s = document.createElement('p');
        s.textContent = LANGUE === 'en'
          ? 'The form is valid. There is no hosting, no sales address and no '
            + 'CRM connected yet, so here is exactly what would be sent:'
          : 'Le formulaire est valide. Il n’y a encore ni hébergement, ni '
            + 'adresse commerciale, ni CRM branché : voici exactement ce qui '
            + 'partirait :';
        var pre = document.createElement('pre');
        pre.style.cssText = 'white-space:pre-wrap;font-size:13px;margin:0;'
          + 'background:#fff;border:1px solid var(--rose-200);'
          + 'border-radius:10px;padding:14px;overflow-x:auto';
        pre.textContent = lignes.join('\n');
        box.appendChild(t); box.appendChild(s); box.appendChild(pre);
        res.appendChild(box);
        res.scrollIntoView({ block: 'nearest' });
      }
    });
  }
})();
