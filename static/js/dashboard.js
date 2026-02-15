function filterPatients(level) {

    let tableContainer = document.getElementById("tableContainer");
    let rows = document.querySelectorAll("#patientTable tr");
    let title = document.getElementById("tableTitle");

    // Show table
    tableContainer.style.display = "block";

    // Change title dynamically
    if(level === "All") {
        title.innerText = "All Patients";
    } else {
        title.innerText = level + " Patients";
    }

    rows.forEach((row, index) => {
        if(index === 0) return;

        if(level === "All") {
            row.style.display = "";
        } else {
            row.style.display = row.dataset.risk === level ? "" : "none";
        }
    });
}
