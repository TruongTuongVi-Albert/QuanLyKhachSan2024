function rent() {
    if (confirm("Bạn chắc chắn thanh toán?") === true) {
        fetch("/api/rent", {
            method: "post"
        }).then(res => res.json()).then(data =>{
            if (data.status === 200)
                location.reload();
            else
                alert("Hệ thống đang có lỗi! Vui lòng quay lại sau!");
        })

    }
}