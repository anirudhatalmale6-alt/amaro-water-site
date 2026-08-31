<?php
/**
 * AMARO — traitement du formulaire « Become an AMARO Distributor ».
 *
 * A DEPOSER a cote des pages, sur l'hebergement. Puis, dans page_amaro.py,
 * mettre ACTION_FORMULAIRE = 'formulaire.php' et reconstruire : le
 * formulaire bascule tout seul de la demonstration au vrai envoi.
 *
 * ────────────────────────────────────────────────────────────────────────
 * TANT QUE $DESTINATAIRE EST VIDE, CE FICHIER REFUSE DE SE DIRE OPERATIONNEL
 * ────────────────────────────────────────────────────────────────────────
 * Il enregistre quand meme la demande — perdre le premier distributeur qui
 * ecrit serait pire — mais il affiche noir sur blanc que personne n'a ete
 * prevenu. Un accuse de reception sans destinataire est le pire des deux
 * mondes : le prospect croit qu'on l'a lu, et personne ne l'a lu.
 */

// ── A REGLER ────────────────────────────────────────────────────────────
$DESTINATAIRE = '';       // l'adresse commerciale AMARO. Vide = non branche.
$EXPEDITEUR   = '';       // une adresse DU DOMAINE, ex. site@votre-domaine
$REGISTRE     = __DIR__ . '/donnees/demandes.sqlite';
$LANGUE       = 'fr';     // 'fr' ou 'en' : la langue des pages de reponse
// ────────────────────────────────────────────────────────────────────────

header('Content-Type: text/html; charset=utf-8');
header('X-Content-Type-Options: nosniff');
header('Referrer-Policy: same-origin');

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
	http_response_code(405);
	exit('Méthode non autorisée.');
}

/* Les champs attendus : nom => obligatoire. La liste est ici, pas dans le
 * HTML : un formulaire poste ce qu'il veut, y compris ce qu'on n'a pas
 * prevu. */
$CHAMPS = array(
	'societe' => true, 'pays' => true, 'ville' => true, 'contact' => true,
	'courriel' => true, 'telephone' => false, 'marches' => true,
	'produits' => false, 'volume' => false, 'message' => false,
);

function propre($v, $max = 500) {
	$v = is_string($v) ? $v : '';
	/* On coupe en CARACTERES, pas en octets : un « é » compte pour deux
	 * octets, et couper au milieu produit un caractere invalide qui casse
	 * l'encodage de tout ce qui suit. */
	$v = preg_replace('/[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]/u', '', $v);
	$v = trim(preg_replace('/[ \t]+/u', ' ', $v));
	return mb_substr($v, 0, $max, 'UTF-8');
}

$donnees = array();
$erreurs = array();

foreach ($CHAMPS as $nom => $requis) {
	$v = propre(isset($_POST[$nom]) ? $_POST[$nom] : '',
	            $nom === 'message' ? 4000 : 300);
	if ($requis && $v === '') { $erreurs[] = $nom; }
	$donnees[$nom] = $v;
}

if ($donnees['courriel'] !== ''
    && !filter_var($donnees['courriel'], FILTER_VALIDATE_EMAIL)) {
	$erreurs[] = 'courriel';
}

/* Les secteurs arrivent en tableau. On ne garde que les valeurs connues :
 * accepter la chaine telle quelle, ce serait laisser un tiers ecrire ce qui
 * atterrit dans le courriel et dans le registre. */
$SECTEURS = array('distributeur', 'grossiste', 'supermarche', 'hotel',
                  'restaurant', 'cafe', 'sport', 'entreprise', 'evenement',
                  'autre');
$secteurs = array();
if (isset($_POST['secteur']) && is_array($_POST['secteur'])) {
	foreach ($_POST['secteur'] as $s) {
		if (in_array($s, $SECTEURS, true)) { $secteurs[] = $s; }
	}
}
if (!$secteurs) { $erreurs[] = 'secteur'; }
$donnees['secteurs'] = implode(', ', $secteurs);

if (empty($_POST['consentement'])) { $erreurs[] = 'consentement'; }

/* Anti-robot : un champ que personne ne voit. S'il est rempli, c'est un
 * automate — et on repond 200 comme si tout allait bien, pour ne pas lui
 * apprendre a quoi ressemble un echec. */
if (!empty($_POST['site_web'])) {
	page('ok', $LANGUE, '');
	exit;
}

if ($erreurs) {
	http_response_code(422);
	page('erreur', $LANGUE, implode(', ', $erreurs));
	exit;
}

// ── Enregistrement ──────────────────────────────────────────────────────
//
// On ecrit AVANT d'essayer d'envoyer. Si le serveur de courriel est en
// panne, la demande est deja sauvee ; l'inverse la perd definitivement.

$reference = 'AMB-' . gmdate('ymd') . '-' . strtoupper(bin2hex(random_bytes(3)));
$enregistre = false;
$souci_registre = '';

try {
	$dossier = dirname($REGISTRE);
	if (!is_dir($dossier)) { @mkdir($dossier, 0750, true); }
	$db = new PDO('sqlite:' . $REGISTRE, null, null, array(
		PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
	));
	/* IF NOT EXISTS, et surtout PAS « si le fichier est absent ». Ouvrir un
	 * fichier SQLite le CREE : un fichier de 0 octet depose par un client FTP
	 * ou par une restauration ferait croire que la table est la, et toute
	 * demande repondrait 500 — pour toujours. */
	$db->exec('CREATE TABLE IF NOT EXISTS demandes (
		id INTEGER PRIMARY KEY, reference TEXT UNIQUE NOT NULL,
		recue_le TEXT NOT NULL, societe TEXT, pays TEXT, ville TEXT,
		contact TEXT, courriel TEXT, telephone TEXT, secteurs TEXT,
		marches TEXT, produits TEXT, volume TEXT, message TEXT,
		ip TEXT, prevenu INTEGER NOT NULL DEFAULT 0)');
	$q = $db->prepare('INSERT INTO demandes (reference, recue_le, societe,
		pays, ville, contact, courriel, telephone, secteurs, marches,
		produits, volume, message, ip)
		VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)');
	$q->execute(array($reference, gmdate('Y-m-d H:i:s'), $donnees['societe'],
		$donnees['pays'], $donnees['ville'], $donnees['contact'],
		$donnees['courriel'], $donnees['telephone'], $donnees['secteurs'],
		$donnees['marches'], $donnees['produits'], $donnees['volume'],
		$donnees['message'],
		isset($_SERVER['REMOTE_ADDR']) ? $_SERVER['REMOTE_ADDR'] : ''));
	$enregistre = true;
} catch (Exception $e) {
	/* Le message d'erreur PDO contient le chemin du fichier : il reste dans
	 * le journal du serveur, il ne part pas dans la page. */
	error_log('AMARO formulaire — registre : ' . $e->getMessage());
	$souci_registre = 'registre';
}

// ── Notification ────────────────────────────────────────────────────────

$prevenu = false;
if ($DESTINATAIRE !== '') {
	$lignes = array('Référence : ' . $reference,
	                'Reçue le : ' . gmdate('Y-m-d H:i:s') . ' UTC', '');
	foreach ($donnees as $k => $v) {
		if ($v !== '') { $lignes[] = ucfirst($k) . ' : ' . $v; }
	}
	$corps = implode("\r\n", $lignes);
	$entetes = array('MIME-Version: 1.0',
	                 'Content-Type: text/plain; charset=UTF-8',
	                 'Content-Transfer-Encoding: 8bit');
	if ($EXPEDITEUR !== '') {
		/* L'expediteur est une adresse DU DOMAINE. Mettre celle du prospect
		 * ferait echouer SPF et DKIM, et le courriel finirait en indesirable
		 * — donc nulle part. Sa vraie adresse va dans Reply-To. */
		$entetes[] = 'From: AMARO <' . $EXPEDITEUR . '>';
	}
	if ($donnees['courriel'] !== '') {
		$entetes[] = 'Reply-To: ' . $donnees['courriel'];
	}
	$sujet = '=?UTF-8?B?' . base64_encode(
		'AMARO Business — ' . $donnees['societe'] . ' (' . $donnees['pays'] . ')')
		. '?=';
	$prevenu = @mail($DESTINATAIRE, $sujet, $corps, implode("\r\n", $entetes));
	if ($prevenu && $enregistre) {
		try {
			$db->prepare('UPDATE demandes SET prevenu = 1 WHERE reference = ?')
			   ->execute(array($reference));
		} catch (Exception $e) { /* sans consequence : la demande est sauvee */ }
	}
}

page($prevenu ? 'ok' : ($enregistre ? 'enregistre' : 'souci'), $LANGUE,
     $reference);


// ── Les pages de reponse ────────────────────────────────────────────────

function page($etat, $langue, $detail) {
	$fr = ($langue !== 'en');
	$titres = array(
		'ok' => $fr ? 'Demande envoyée' : 'Enquiry sent',
		'enregistre' => $fr ? 'Demande enregistrée' : 'Enquiry recorded',
		'souci' => $fr ? 'Demande reçue' : 'Enquiry received',
		'erreur' => $fr ? 'Formulaire incomplet' : 'Incomplete form',
	);
	$textes = array(
		'ok' => $fr
			? 'Votre demande a bien été transmise à l’équipe commerciale AMARO. '
			  . 'Référence : ' . htmlspecialchars($detail) . '.'
			: 'Your enquiry has been sent to the AMARO sales team. Reference: '
			  . htmlspecialchars($detail) . '.',
		/* L'etat le plus important du fichier : la demande est SAUVEE, et
		 * personne n'a ete prevenu. On le dit, on ne le maquille pas. */
		'enregistre' => $fr
			? 'Votre demande est enregistrée sous la référence '
			  . htmlspecialchars($detail) . '. Aucune notification n’a pu être '
			  . 'envoyée : l’adresse commerciale n’est pas encore configurée sur '
			  . 'ce site. La demande n’est pas perdue, elle attend dans le '
			  . 'registre.'
			: 'Your enquiry is recorded under reference '
			  . htmlspecialchars($detail) . '. No notification could be sent: '
			  . 'the sales address is not configured on this site yet. The '
			  . 'enquiry is not lost, it is waiting in the register.',
		'souci' => $fr
			? 'Votre demande n’a pas pu être enregistrée sur le serveur. '
			  . 'Merci de réessayer, ou de nous joindre autrement.'
			: 'Your enquiry could not be recorded on the server. Please try '
			  . 'again, or reach us another way.',
		'erreur' => $fr
			? 'Certains champs obligatoires sont absents ou invalides : '
			  . htmlspecialchars($detail) . '. Revenez en arrière pour les '
			  . 'compléter.'
			: 'Some required fields are missing or invalid: '
			  . htmlspecialchars($detail) . '. Go back to complete them.',
	);
	$t = $titres[$etat];
	$p = $textes[$etat];
	echo '<!DOCTYPE html><html lang="' . ($fr ? 'fr' : 'en') . '"><head>'
	   . '<meta charset="utf-8"><meta name="viewport" '
	   . 'content="width=device-width,initial-scale=1">'
	   . '<title>' . $t . ' — AMARO</title>'
	   . '<link rel="stylesheet" href="styles.css"></head><body>'
	   . '<main id="contenu"><section class="section"><div class="enveloppe">'
	   . '<div class="tete"><h2>' . $t . '</h2><p>' . $p . '</p></div>'
	   . '<a class="btn btn--plein" href="index.html">'
	   . ($fr ? 'Retour à l’accueil' : 'Back to home') . '</a>'
	   . '</div></section></main></body></html>';
}
