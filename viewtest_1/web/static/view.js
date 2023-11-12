document.addEventListener("DOMContentLoaded", function () {
  document.querySelector("#vForm").addEventListener("submit", function (e) {
      e.preventDefault();  // 阻止默認的表單提交行為
      const form = e.target;
      const formData = new FormData(form);
      fetch("/vdata", {
        method: "POST",
        body: formData,
      })
      .then(response => response.json())
      .then(data => {
        // 在此處理回應資料，可以顯示成功消息或執行其他操作
        //const MessageLabel = document.getElementById("message2");
        //const newMessage = data.replace( /&/g , "<br>");
        //MessageLabel.innerHTML = newMessage;

        let viewBody = document.getElementById("viewTable").getElementsByTagName("tbody")[0];
        
        // 清空tbody，以防之前的數據仍在
        viewBody.innerHTML = "";

        // 遍歷數據陣列，每個元素都是一行
        data.forEach(appointment => {
          // 創建新的表格行
          let row = viewBody.insertRow();

          let startTimeCell = row.insertCell();
          startTimeCell.textContent = appointment["r_start"];  // 第一項是開始時間

          let endTimeCell = row.insertCell();
          endTimeCell.textContent = appointment["r_end"];  // 第二項是結束時間

          let attendeeCell = row.insertCell();
          attendeeCell.textContent = appointment["c_id"];  // 第三項是預約人

          let meetingRoomCell = row.insertCell();
          meetingRoomCell.textContent = appointment["room_no"];  // 第四項是會議室
        });
      })
      .catch(error => {
        console.error("Error:", error);
      });
  });
});