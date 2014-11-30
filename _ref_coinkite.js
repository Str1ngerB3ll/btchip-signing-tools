// (c) Copyright 2014 by Coinkite Inc.
//
// May require:
//  Crypto-JS AES rollup (3.1.2) (in global namespace as "bitcoin")
//  BIP39 code (in global namespace as "BIP39")
//  Buffer code (in global namespace as "COINKITE.Buffer")
//
// This section has been kept un-minimized for your debug and voyeuristic pleasure.
//

ARGS = {};
CCT_NETWORK = 0;

Buffer = COINKITE.Buffer;
assert = COINKITE.ASSERT;

function die_now(msg) {
    $("body").html("<pre>" + msg);
    throw "fatal error";
}

function parseQuery(qstr) {
    // from http://stackoverflow.com/questions/2090551
    var query = {},
        a = qstr.split('&');
    for (var i in a) {
        var b = a[i].split('=');
        query[decodeURIComponent(b[0])] = decodeURIComponent(b[1]);
    }

    return query;
}


$(document).ready(function() {
    // Setup code

    // Look at some optional args.
    ARGS = parseQuery(window.location.search.substring(1));

    // what network are we on?
    ARGS.cct = ARGS.cct || 'BTC';

    var nets = bitcoin.networks;
    var warn = false;
    if (ARGS.cct == 'BTC') {
        CCT_NETWORK = nets.bitcoin;
    } else if (ARGS.cct == 'XTN') {
        CCT_NETWORK = nets.testnet;
        warn = "Testnet3"
    } else if (ARGS.cct == 'LTC') {
        CCT_NETWORK = nets.litecoin;
        warn = "Litecoin"
    } else {
        // caution XSS: don't repeat arg in message.
        die_now("This code doesn't support that kind of crypto currency (yet?)");
    }
    if (warn) {
        $('.js-other-cct-warning .cctname').text(warn);
    } else {
        $('.js-other-cct-warning').hide();
    }

    // do some helpful rollovers
    $('.rolltip').tooltip();
});



// Well-known message signing key for Coinkite.com
CK_SIGNING_ADDRESS = '1GPWzXfpN9ht3g7KsSu8eTB92Na5Wpmu7g';

// Where to send final data, iff we downloaded it initally successfully from there.
SUBMIT_URL = null;

REQUEST_DATA = null;
RESPONSE = null;

XPRIVKEY = null;

function setup_req(q) {
    //console.log("Req: ", q);

    // show the request, and prepare to sign it.
    $('.js-proposal-html').html(q.proposal_html);
    $('.js-proposal-title').text(q.proposal_title);
    $('.js-proposal-tech').html(q.super_tech_html);
    $('.js-proposed-txn').show();

    $('.js-req-xpubkey').text(q.xpubkey_display);
    $('.js-req-xpubkey-check').text(q.xpubkey_check);

    REQUEST_DATA = q;
}

function check_file_signature(data) {
    var wrap = data;

    if (typeof(data) == 'string') {
        // expects JSON, in my own format
        try {
            wrap = JSON.parse(data);
        } catch (e) {
            return "Corrupt JSON data";
        }
    }

    if (!wrap.contents || !wrap.signed_by || !wrap.signature) {
        return "Bad file contents or signature missing!";
    }

    if (wrap.signed_by != CK_SIGNING_ADDRESS) {
        return "Wrong signing key!?";
    }

    var ok = bitcoin.Message.verify(CK_SIGNING_ADDRESS, wrap.signature, wrap.contents)

    if (!ok) {
        return "Request data failed signature verification. Might be tampered with!";
    }

    // safe now to look inside contents
    try {
        var q = JSON.parse(wrap.contents)
    } catch (e) {
        return "Server gave corrupt JSON data";
    }

    try {
        setup_req(q);
    } catch (e) {
        return "Internal issues with signing request";
    }

    $('.js-need-file').hide()
    $('.js-downloading').hide()
    $('.js-step1').hide()
    $('.js-step2').show()
    $('.step-label').removeClass('active');
    $('.step-label.step2').addClass('active');
}

function reset_ui_state() {
    // stupoood crap we need
    $('.js-proposed-txn').hide();
    $('.js-step1').show();
    $('.js-step2').hide();
    $('.js-step3').hide();
    $('.js-step4').hide();
    $('.js-need-file').show();
    $('.js-downloading').hide();
    $('.js-upload-good').hide();
    $('.js-cant-upload').hide();
    $('.js-upload-busy').hide();

    $('.step-label').removeClass('active');
    $('.step-label.step1').addClass('active');
}

function prompt_password(encrypted) {
    var mod = $('#passphrase-modal');

    mod.on('shown.bs.modal', function(e) {
        mod.find('.js-password').focus();
    })

    mod.data('enc-file', encrypted);
    mod.modal('show');
}

function got_password(event) {
    // never want to "submit" this form
    // cross-browser issues here w/ FF
    event = event || window.event;
    if (event) {
        event.preventDefault();
    }

    var mod = $('#passphrase-modal');
    var pw = mod.find('.js-password').val();
    mod.find('.js-password').val(''); // clear it always
    var feedback = $('.js-keyfile-feedback');

    var file = mod.data('enc-file');
    try {
        var decode = CryptoJS.AES.decrypt(file, pw).toString(CryptoJS.enc.Utf8);
    } catch (e) {
        // typically get a "malformed UTF-8 data" here.
        feedback.text("File did not decrypt correctly. Wrong passphrase?");

        return;
    }

    mod.modal('hide');

    if (decode.match(/[xt]prv/)) {
        feedback.text(import_key_file(decode));
    } else {
        feedback.text("File did not contain useful stuff? Wrong passphrase?");
    }
}

function import_key_file(data) {
    // parse a key file; which might be just a xprvkey or our OpenSSL encrypted file.

    if (data.length < 100) {
        return "File size was too small.";
    }

    var xpubkey = data.match(/.*(^[xt]pub\S*)/gm);
    if (xpubkey) xpubkey = xpubkey[1];

    var encrypted = data.replace(/\n/gm, '').match(/(U2FsdGVkX.*)(\^\^\^)/);
    if (encrypted) encrypted = encrypted[1];

    var xprivkey = data.match(/.*(^[xt]prv\S*)/gm);
    if (xprivkey) xprivkey = xprivkey[0];

    if (!xprivkey && !xpubkey && !encrypted) {
        return "Could not understand file. Should contain an xpubkey / xprvkey and/or encrypted same";
    }

    if (xprivkey || xpubkey) {
        // test that's it what we need today.
        try {
            var node = bitcoin.HDNode.fromBase58(xprivkey ? xprivkey : xpubkey);
        } catch (e) {
            return "Invalid characters in base58 or corrupted data.";
        }
        var check = node.neutered().toBase58();
        var l = check.length;
        if (check.substr(l - 8, 8) != REQUEST_DATA.xpubkey_check) {
            return "Wrong key. We need the private key that corresponds to an xpubkey ending in ..." + REQUEST_DATA.xpubkey_check;
        }

        xpubkey = check;
    }

    if (!xprivkey) {
        if (!encrypted) {
            return "We require either xprvkey or OpenSSL encrypted backup file of that.";
        }

        // we'll come back into here after they enter the P/W.
        prompt_password(encrypted);

        return "Need correct file passphrase.";
    }

    XPRIVKEY = xprivkey;

    // make feeble attempt to clear sensitive data
    $('.js-xprv-paste-area').remove(); // impt: kills events too
    $('#passphrase-modal').data('enc-file', 'consumed');

    $('.js-step2').hide()
    $('.js-step3').show()

    $('.step-label').removeClass('active');
    $('.step-label.step3').addClass('active');

    return 'Good keyfile!';
}

function new_xprivkey() {
    // clean up a bit
    var pp = $(this).val().replace(/\s/gm, '');

    var feedback = $('.js-keyfile-feedback');
    feedback.text('');

    if (pp.match(/[tx]prv/)) {
        feedback.text(import_key_file(pp));
    } else {
        feedback.text(pp.length ? "Invalid xprv key data" : "");
    }
}

function open_key_file(event) {
    // They have provided some sort of file with the private key inside
    var files = event.target.files;
    var ele = $(event.target);

    if (!files || files.length <= 0) {
        console.log("No files picked");
        return;
    }

    // read the file's contents.
    var reader = new FileReader();

    var f = files[0];
    var feedback = $('.js-keyfile-feedback');

    // callback for when data is loaded
    reader.onload = function(data) {
        var data = reader.result;

        feedback.text(import_key_file(data));
    };

    // Read in the file as a string. 
    reader.readAsText(f);
}

function open_req_file(event) {
    // User is providing our complex, signed JSON file from local filesystem.

    // see http://www.html5rocks.com/en/tutorials/file/dndfiles/
    event = event || window.event;
    var files = event.target.files;
    var ele = $(event.target);

    if (!files || files.length <= 0) {
        console.log("No files picked");
        return;
    }

    // read the file's contents.
    var reader = new FileReader();

    var f = files[0];
    var feedback = $(ele).parent().parent().find('.js-file-feedback');

    // callback for when data is loaded
    reader.onload = function(data) {
        // show filename in UI

        var data = reader.result;
        if (data.length < 100) {
            feedback.text("File size was too small.");

            return;
        }

        var prob = check_file_signature(data);
        if (prob) {
            feedback.text(prob);
        } else {
            feedback.text("Loaded and verified file okay.")
        }
    };

    // Read in the file as a string. 
    reader.readAsText(f);
}

function approve_txn() {
    // Time to sign!
    var rv = {
        cosigner: REQUEST_DATA.cosigner,
        request: REQUEST_DATA.request
    };

    // XXX progress/heartbeat

    // Make a "wallet" of each subkey we'll need
    var subpaths = Object.keys(REQUEST_DATA.req_keys);
    var root = bitcoin.HDNode.fromBase58(XPRIVKEY)
    var wallets = {};
    for (var i = 0; i < subpaths.length; i++) {
        var sp = subpaths[i];

        // TODO: split on slash, go deeper for subpaths.
        var w = root.derive(Number(sp));

        // check math
        var check_pk = w.getAddress().toBase58Check();
        var expect_pk = REQUEST_DATA.req_keys[sp][0];

        assert.equal(check_pk, expect_pk, "Got wrong wallet at: " + sp);

        wallets[sp] = w;
    }

    // Do a signing, for every input on the transaction
    var ins = REQUEST_DATA.inputs;
    var sigs = new Array();
    for (var idx = 0; idx < ins.length; idx++) {
        var sp = ins[idx][0];
        var sighash = Buffer(ins[idx][1], 'hex');
        var private_key = wallets[sp].privKey;

        sigs.push([
            private_key.sign(sighash).toScriptSignature(1).toString('hex'),
            sighash.toString('hex'),
            sp
        ]);
    }

    rv.signatures = sigs;

    // wrap with a signature.
    var body = {
        _humans: "Upload this set of signatures to Coinkite.",
        content: JSON.stringify(rv)
    };

    // always use the bitcoin version of the signature.
    body.signature = bitcoin.Message.sign(root.privKey, body.content,
        bitcoin.networks.bitcoin).toString('base64');
    body.signed_by = root.pubKey.getAddress(bitcoin.networks.bitcoin).toBase58Check();

    RESPONSE = JSON.stringify(body);

    $('.js-step3').hide();
    $('.js-step4').show();

    // always try an upload next
    upload_to_ck();
}

function ck_upload_fail(prob) {
    $("#upload_btn").removeClass('btn-primary');
    $('.js-ck-upload-prob').text(prob);
    $('.js-cant-upload').show()
    $('.js-upload-busy').hide()
}

function upload_to_ck() {
    $('.js-upload-busy').show()

    $.ajax({
        type: "PUT",
        url: '/co-sign/done-signature',
        data: RESPONSE,
        contentType: 'text/plain'
    }).done(function(resp) {
        // Expect a short string reponse, either a URL to visit, "DONE" or an error msg.
        $('.js-upload-busy').hide()

        if (resp == 'DONE') {
            // success case; nothing more to do
            $('.js-cant-upload').hide()
            $('.js-upload-good').show();
            $('.js-goto-ck').hide();

            try {
                // attempt reload of original page; so it shows new key in place.
                window.opener.location.reload();
            } catch (e) { /* dont care */ };
        } else if (resp[0] == '/') {
            $('.js-upload-good').hide();
            $('.js-goto-ck').show();
            $('.js-cant-upload').hide()
            $('.js-goto-ck a').attr({
                'href': 'https://coinkite.com' + resp
            });
        } else {
            ck_upload_fail(resp);
        }
    }).fail(function() {
        ck_upload_fail("File upload failed with an error from server.");
    });
}

function save_to_file() {
    // see http://eligrey.com/blog/post/saving-generated-files-on-the-client-side/

    saveAs(new Blob([RESPONSE], {
        type: "text/plain"
    }), "signed-transaction.txt");
}

function show_warnings() {
    // from btn in footer
    $('.js-warnings-area').removeClass('hide');
    $('.js-warnings-area').toggle();
}

$(document).ready(function() {
    // Setup code

    /*
        // not able to hide with css class at start?!? workaround.
        $('.js-rnd-done').hide();
        $('.js-file-ready').hide();
        $('.js-cant-upload').hide();
        $('.js-upload-good').hide();
        $('.js-goto-ck').hide();
    */
    reset_ui_state();

    if (ARGS.json && location.protocol != 'file:') {
        // load the request file. attempt to work over Tor or HTTPS
        var url = location.protocol + '//' + location.host + ARGS.json;

        $('.js-downloading').show();
        $('.js-need-file').hide();

        console.log("Fetching: " + url);
        var feedback = $('.js-need-file .js-file-feedback');

        $.getJSON(url, function(data) {
            // success.
            var prob = check_file_signature(data);
            if (prob) {
                // show unlikely error
                $('.js-need-file').show();
                $('.js-downloading').hide();
                feedback.text(prob);
            } else {
                // UI already has been moved to next step
                SUBMIT_URL = url;
            }
        }).fail(function(jqh) {
            var resp = jqh.responseText;
            $('.js-need-file').show();
            $('.js-downloading').hide();
            if (resp.length && resp.length < 200) {
                feedback.text(resp);
            }
        });
    }

    // track paste into textarea
    $('textarea.xprv-paste-area').on('keyup', new_xprivkey);
    $('textarea.xprv-paste-area').on('change', new_xprivkey);

    $('.js-startup-failed').hide(); // keep last

    // connecting events using jQuery is more reliable cross-browser compared to
    // using HTML markup.
    $('input.js-keyfile-uploader').on('change', open_key_file);
    $('input.js-file-uploader').on('change', open_req_file);

    $('#pp-form').on('submit', got_password);
    $('button.pp-form-submit').on('click', got_password);
});
