function addClick(ad_slug) {
    fetch("/ad_click/" + ad_slug, {
        method: "GET",
        headers: {
          "X-Requested-With": "XMLHttpRequest",
        },
      }).then(data => {
        if (data.success === 'true') {
            window.location.href = url;
        }
    })
}