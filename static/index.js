function dropDownShow(id, value) {
    document.getElementById(id).innerHTML = value + '\n';
    let s ='../static/resource/'+value+'.jpg'
    console.log(s)
    $("#img").attr("src",s)
}

function dropDownShows(id, value) {
    document.getElementById(id).innerHTML = value + '\n';
}

let KEY = "Click on ciphertext to show";

function generateKeypair() {
    const kl = document.getElementById("kl").innerHTML.replace("\n", "");
    if (isNaN(parseInt(kl))) {
        alert("Key Length is not a number");
        return null;
    }

    $.ajax({
        url: '/gk',
        method: 'POST',
        data: {
            kl: kl,
        },
        success: function (data) {
            alert("Keypair [" + kl + "] generation succeeded");
            KEY = data.kp;
            document.getElementById('kp').value = data.kp;
        }
    })
}

function encryption() {
    const p1 = document.getElementById('p1').value;
    const p2 = document.getElementById('p2').value;
    if (isNaN(parseInt(p1)) || isNaN(parseInt(p2))) {
        alert("Plaintext 1 or Plaintext 2 is not a number");
        return null;
    }
    $.ajax({
        url: '/enc',
        method: 'POST',
        data: {
            p1: p1,
            p2: p2,
        },
        success: function (data) {
            alert("Plaintext [" + p1 + "] and [" + p2 + "] are encrypted");
            document.getElementById('c1').value = data.c1;
            document.getElementById('c2').value = data.c2;
        }
    })
}

function calculation() {
    const p1 = document.getElementById('p1').value;
    const p2 = document.getElementById('p2').value;
    const ptc = document.getElementById('ptc').innerHTML.replace("\n", "");
    if (isNaN(parseInt(p1)) || isNaN(parseInt(p2))) {
        alert("Plaintext 1 or Plaintext 2 is not a number");
        return null;
    }
    $.ajax({
        url: '/cal',
        method: 'POST',
        data: {
            p1: p1,
            p2: p2,
            ptc: ptc,
        },
        success: function (data) {
            if (data.cr === '') {
                alert("[Protocol] is not a protocol");
                return null;
            }
            alert("[" + ptc + "] is calculated");
            document.getElementById('cr').value = data.cr;
        }
    })
}

function decryption() {
    const c1 = document.getElementById('c1').value;
    if (isNaN(parseInt(c1))) {
        alert("Ciphertext Result is empty");
        return null;
    }
    $.ajax({
        url: '/dec',
        method: 'POST',
        success: function (data) {
            alert("Ciphertext Result is decrypted");
            document.getElementById('dr').value = data.dr;
        }
    })
}

function showText(id) {
    if (id === 'kp') {
        document.getElementById('show').innerHTML = KEY;
    } else {
        document.getElementById('show').innerHTML = document.getElementById(id).value;
    }
}
