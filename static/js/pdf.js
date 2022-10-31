window.addEventListener('load', () => {
    
    const name = localStorage.getItem('NAME');
    const age = localStorage.getItem('AGE');
    const email = localStorage.getItem('EMAIL');
    const diesease = localStorage.getItem('DISEASE');
    
    
    document.getElementById('result-name').innerHTML = name;
    document.getElementById('result-age').innerHTML = age;
    document.getElementById('result-email').innerHTML = email;
    document.getElementById('result-diesease').innerHTML = diesease;
    

})

window.onload = function () {
    document.getElementById("download")
        .addEventListener("click", () => {
            const invoice = this.document.getElementById("invoice");
            console.log(invoice);
            console.log(window);
            var opt = {
                margin: 1,
                filename: 'Diagnose Report.pdf',
                image: { type: 'jpeg', quality: 0.98 },
                html2canvas: { scale: 2 },
                jsPDF: { unit: 'in', format: 'tabloid', orientation: 'portrait' }
            };
            html2pdf().from(invoice).set(opt).save();
        })
}