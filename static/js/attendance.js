function openAttendanceModal() {
    document.getElementById("attendanceModal").style.display = "block";
}

function closeAttendanceModal() {
    document.getElementById("attendanceModal").style.display = "none";
}

window.onclick = function(event) {
    const modal = document.getElementById("attendanceModal");
    if (event.target == modal) {
        modal.style.display = "none";
    }
}
