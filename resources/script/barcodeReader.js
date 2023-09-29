// OpenCV.jsを読み込み、初期化します
let Module = {
    onRuntimeInitialized: function () {
        // カメラからビデオストリームを取得
        navigator.mediaDevices.getUserMedia({
            video: {
                facingMode: 'environment',
                height: {
                    min: 720,
                    ideal: 1080,
                    max: 1440
                },
                width: {
                    min: 720,
                    ideal: 1080,
                    max: 1440
                }
            }
        })
            .then(function (stream) {
                let video = document.getElementById('video');
                video.srcObject = stream;
                video.play();

                // カメラの設定を取得
                const settings = stream.getVideoTracks()[0].getSettings();

                // オートフォーカスを有効にする場合
                if ('focusMode' in settings) {
                    settings.focusMode = 'continuous';
                    stream.getVideoTracks()[0].applyConstraints({ advanced: [settings] })
                        .then(function () {
                            console.log('オートフォーカスを有効にしました。');
                        })
                        .catch(function (error) {
                            console.error('オートフォーカスの設定に失敗しました: ', error);
                        });
                }

                // バーコードを読み取る関数を呼び出します
                readBarcodeFromVideoDevice(video);
            })
            .catch(function (error) {
                console.error('カメラへのアクセスが拒否されました: ', error);
            });
    }
};

// ビデオデバイスからバーコードをリアルタイムで読み取る関数
function readBarcodeFromVideoDevice(video) {
    const codeReader = new ZXing.BrowserMultiFormatReader();
    const videoElement = document.getElementById('video');
    const barcodeValueElement = document.getElementById('barcodeValue'); // バーコードの値を表示する要素

    // ビデオフレームからバーコードを読み取るループ
    function scanBarcode() {
        codeReader.decodeFromVideoDevice(undefined, videoElement, (result, err) => {
            if (result) {
                const barcodeValue = result.text;
                barcodeValueElement.textContent = 'バーコード: ' + barcodeValue; // バーコードの値を表示
            }
            if (err) {
                //console.error('バーコード読み取りエラー:', err);
            }

            // 次のフレームで再びバーコードを読み取る
            //requestAnimationFrame(scanBarcode);
        });
    }

    // バーコード読み取りを開始
    scanBarcode();
}
