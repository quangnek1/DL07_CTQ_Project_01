import streamlit as st
import pandas as pd
import pickle
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import os
from PIL import Image
from utils import TongHopTienXuLy



# Menu
st.set_page_config(page_title="DL07 CTQ Project 1", layout="wide")
menu = ["Home", "Capstone Project", "Sử dụng các điều khiển", "Hiển thị chart"]
# st.sidebar.image("path_to_your_logo.png", use_column_width=True)
st.sidebar.markdown("<h1 style='font-size: 24px;'>DL07 CTQ Project 1</h1>", unsafe_allow_html=True)
choice = st.sidebar.selectbox('Menu', menu)

# CSS cho cuộn mượt và căn chỉnh
# st.markdown("""<style>html {scroll-behavior: smooth; /* Cuộn mượt */}section {margin-bottom: 50px;padding: 20px;border-bottom: 1px solid #ccc; /* Đường ngăn cách */}h2 {color: #FF4B4B; /* Màu đỏ cho tiêu đề */}</style>""", unsafe_allow_html=True)

# Nội dung từng phần
st.markdown("<section id='business-understanding'>", unsafe_allow_html=True)
st.header("Sentiment Analysis")
st.write("Phân tích cảm nghĩ, đánh giá, phản hồi bình luận.")
st.markdown("</section>", unsafe_allow_html=True)

# Ô nhập liệu
user_input = st.text_area("Nhập đánh giá của bạn:", placeholder="Ví dụ: Sản phẩm rất tuyệt vời!")
# Tải mô hình và TF-IDF Vectorizer
with open('logistic_regression_model.pkl', 'rb') as f_model:
    loaded_model = pickle.load(f_model)

with open('tfidf_vectorizer.pkl', 'rb') as f_vectorizer:
    loaded_vectorizer = pickle.load(f_vectorizer)



# Xử lý khi người dùng nhấn nút "Dự đoán"
if st.button("Dự đoán"):
    if user_input.strip() == "":
        st.warning("Vui lòng nhập đánh giá.")
    else:
        # Tiền xử lý văn bản
        preprocessed_review = TongHopTienXuLy(user_input)
        # Đánh giá mới cần dự đoán

        # Biến đổi đánh giá mới thành TF-IDF vector
        new_review_vectorized = loaded_vectorizer.transform([preprocessed_review])

        # Dự đoán sentiment
        predicted_sentiment = loaded_model.predict(new_review_vectorized)
        predicted_probabilities = loaded_model.predict_proba(new_review_vectorized)

        # Hiển thị kết quả
         # Hiển thị kết quả
        st.subheader("Kết quả phân tích:")
        print("Predicted Sentiment:", predicted_sentiment[0])
        st.write(predicted_sentiment[0])
       
       
         


# Open and read file to cosine_sim_new
with open('products_cosine_sim.pkl', 'rb') as f:
    cosine_sim_new = pickle.load(f)



# Thêm CSS để tạo giao diện giống như ảnh
# Hàm load CSS
def load_css(file_name):
    with open(file_name, "r") as f:
        return f"<style>{f.read()}</style>"
# Chèn CSS từ file style.css
st.markdown(load_css("style.css"), unsafe_allow_html=True)
st.markdown(
    """
    <style>
    .header hr {
        border: 1px solid #00d7ff; /* Đường kẻ màu xanh */
        width: 100%;
        margin: 10px auto;
    }

    .sub-header {
        text-align: left;
        font-size: 14px;
        color: #cccccc;
        margin-bottom: 30px;
    }

    .card {
        background-color: #262626; /* Màu nền từng card */
        border-radius: 8px;
        padding: 20px;
        text-align: left;
        box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2);
    }

    .card h2 {
        font-size: 18px;
        color: #ffae00; /* Màu chữ chính */
        margin-bottom: 10px;
    }

    .card h3 {
        font-size: 14px;
        color: #ff4b4b; /* Màu chữ nhỏ (điểm nhấn) */
    }

    .card p {
        font-size: 13px;
        color: #cccccc;
        line-height: 1.6;
        margin: 10px 0;
    }

    .card button {
        background-color: #ff4b4b;
        color: white;
        border: none;
        padding: 10px 15px;
        font-size: 12px;
        border-radius: 4px;
        cursor: pointer;
        text-align: center;
        margin-top: 10px;
    }

    .card button:hover {
        background-color: #ff6b6b;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Tạo tiêu đề
st.markdown(
    """
    <div class="container">
        <div class="header">
            <h1>Source Overview</h1>
            <hr>
        </div>
        <div class="sub-header">
            Tổng quan về dự án được thể hiện qua những nội dung dưới đây:
        </div>
        <div class="content">
            <div class="card">
                <h2>Business Understanding</h2>
                <h3>HTTPS://HASAKI.VN</h3>
                <p>Hasaki là thương hiệu phân phối mỹ phẩm nổi tiếng tại Việt Nam</p>
                <p>Hỗ trợ Hasaki cải thiện sản phẩm/dịch vụ từ phản hồi của khách hàng</p>
                <button>View More</button>
            </div>
            <div class="card">
                <h2>Data Understanding</h2>
                <h3>Danh_gia.csv</h3>
                <p>Bài toán sentiment analysis tập trung vào hai cột chính trong tệp Danh_gia.csv</p>
                <p>Negative và Neutral chiếm tỷ lệ rất nhỏ, nhưng lại quan trọng trong việc phát hiện...</p>
                <button>View More</button>
            </div>
            <div class="card">
                <h2>Data Preparation</h2>
                <h3>Underthesea library</h3>
                <p>Underthesea là một toolkit hỗ trợ cho việc nghiên cứu và phát triển xử lý ngôn ngữ tự nhiên tiếng Việt.</p>
                <button>View More</button>
            </div>
            <div class="card">
                <h2>Modeling & Evaluation (for ML)</h2>
                <h3>Logistic Regression</h3>
                <p>Hồi quy Logistic là một mô hình thống kê được sử dụng để phân loại nhị phân, tức dự đoán một đối tượng thuộc vào một trong hai nhóm. Hồi quy Logistic làm việc dựa trên nguyên tắc của hàm sigmoid.</p>
                <button>View More</button>
            </div>
            <div class="card"">
                <h2>Analyze & Report</h2>
                <h3>31% (and growing) are chatbots</h3>
                <p>Chatbots let users iteratively refine answers, creating fluid, human-like conversations with the LLM.</p>
                <button>Are chatbots the future?</button>
            </div>
              <div class="card">
                <h2>Deployment & Feedback/ Act</h2>
                <h3>31% (and growing) are chatbots</h3>
                <p>Chatbots let users iteratively refine answers, creating fluid, human-like conversations with the LLM.</p>
                <button>Are chatbots the future?</button>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Business Understanding
# Đường dẫn tuyệt đối đến thư mục chứa hình ảnh
current_dir = os.path.dirname(os.path.abspath(__file__))
image_path = os.path.join(current_dir, "logo.jpg")

sidebarlogo = Image.open('logo.jpg').resize((100, 50))


# Tạo tiêu đề
st.markdown(
    """
    <div class="container">
        <div class="header">
            <h1>Business Understanding</h1>
            <hr>
        </div>
        <div class="sub-header">
            Tổng quan về Business: <a style="color: #77d777;" href="https://hasaki.vn/">https://hasaki.vn</a>
        </div>
        <div class="content">
    """,
    unsafe_allow_html=True,
)
st.image(sidebarlogo, use_container_width=False)
st.markdown(
    """
    <h3>Bối cảnh:</h3>
    <ul>
    <li>HASAKI.VN là hệ thống cửa hàng mỹ phẩm chính hãng và dịch vụ chăm sóc sắc đẹp chuyên sâu với hệ thống cửa hàng trải dài trên toàn quốc; và hiện đang là đối tác phân phối chiến lược tại thị trường Việt Nam của hàng loạt thương hiệu lớn...</li>
    <li>Khách hàng có thể lên đây để lựa chọn sản phẩm, xem các đánh giá/ nhận xét cũng như đặt mua sản phẩm.</li>
    <li>Từ những đánh giá của khách hàng, vấn đề được đưa ra là làm sao để các nhãn hàng hiểu khách hàng rõ hơn, biết họ đánh giá gì về sản phẩm, từ đó có thể cải thiện chất lượng sản phẩm cũng như các dịch vụ đi kèm.</li>
    </ul>
    <h3>Vấn đề:</h3>
    <ul><li>Các đánh giá thường ở dạng văn bản thô, gây khó khăn trong việc phân tích.</li></ul>
    
    <h3>Mục tiêu:</h3>
    <ul>
    <li>Phân loại cảm xúc (Sentiment Analysis).</li>
    <li>Cải thiện tốc độ và độ chính xác bằng cách tự động hóa phân tích đánh giá.</li>
    <li>Hỗ trợ Hasaki cải thiện sản phẩm/dịch vụ từ phản hồi của khách hàng.</li>
    </ul>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# Tạo tiêu đề
st.markdown(
    """
    <div class="container">
        <div class="header">
            <h1>Data Understanding</h1>
            <hr>
        </div>
        <div class="sub-header">
            Tổng quan về BData Understanding:
        </div>
        <div class="content">
    """,
    unsafe_allow_html=True,
)
 
st.markdown(
    """
    <h3>Dữ liệu cung cấp:</h3>
    <ul>
    <li>San_pham.csv: Thông tin về sản phẩm.</li>
    <li>Khach_hang.csv: Thông tin về khách hàng.</li>
    <li>Danh_gia.csv: Chứa các đánh giá của khách hàng.</li>
    </ul>
    <h3>Dữ liệu trọng tâm:</h3>
    <ul><li>Bài toán sentiment analysis tập trung vào hai cột chính trong tệp Danh_gia.csv.</li></ul>
     """,
    unsafe_allow_html=True,
)
# Data Understanding
# Đường dẫn đến các file CSV
current_dir = os.path.dirname(os.path.abspath(__file__))
danh_gia_path = os.path.join(current_dir, "Danh_gia.csv")
khach_hang_path = os.path.join(current_dir, "Khach_hang.csv")
san_pham_path = os.path.join(current_dir, "San_pham.csv")

# Đọc các file CSV vào DataFrame
danh_gia = pd.read_csv(danh_gia_path)
khach_hang = pd.read_csv(khach_hang_path)
san_pham = pd.read_csv(san_pham_path)

# Merge dữ liệu
merged_data_1 = danh_gia.merge(khach_hang, on='ma_khach_hang', how='left')
final_data = merged_data_1.merge(san_pham, on='ma_san_pham', how='left')

# Đổi tên các cột
final_data.rename(columns={
    'ma_khach_hang': 'Ma_khach_hang',
    'ho_ten': 'Ho_ten',
    'ma_san_pham': 'Ma_san_pham',
    'ten_san_pham': 'Ten_san_pham',
    'noi_dung_binh_luan': 'Noi_dung_binh_luan',
    'ngay_binh_luan': 'Ngay_binh_luan',
    'so_sao': 'So_sao'
}, inplace=True)

# Lựa chọn các cột cần thiết
final_data = final_data[['Ma_khach_hang', 'Ho_ten', 'Ma_san_pham', 'Ten_san_pham',
                         'Noi_dung_binh_luan', 'Ngay_binh_luan',
                         'So_sao']]

# Hiển thị kết quả
# Hàm để tạo kiểu cho cột cụ thể
def highlight_columns(s):
    return ['background-color: yellow; border: 2px solid red;' if s.name in ['Noi_dung_binh_luan', 'So_sao'] else '' for v in s]

# Áp dụng kiểu cho DataFrame
styled_df = final_data.head().style.apply(highlight_columns, axis=0)

# Hiển thị DataFrame với kiểu đã áp dụng
st.dataframe(styled_df)



st.markdown(
    """
    <h3>Tổng quan dữ liệu:</h3>
    <span>Xử lý dữ liệu Null:</span>
    <ul>
    <li>Phương án: Xóa các dòng dữ liệu Null trong cột Noi_dung_binh_luan</li>
    </ul>
        </div>
            """,
    unsafe_allow_html=True,
)
image_path_beforeAfterNull = os.path.join(current_dir, "beforeAfterNull.jpg")
st.image(image_path_beforeAfterNull, use_container_width=True)

st.markdown(
    """
    <p style:"text-align: center;"><i>Hình: Trước và sau khi xử lý null trong cột Noi_dung_binh_luan và So_sao</i></p>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <h3>Xem phân phối số liệu:</h3>
    <h5>Xem phân phối độ dài bình luận:</h5>
    <ul>
    <li>Số sao 5 chiếm phần lớn dữ liệu, Positive chiếm ưu thế lớn</li>
    <li>Negative và Neutral chiếm tỷ lệ rất nhỏ, nhưng lại quan trọng trong việc phát hiện vấn đề và cải thiện dịch vụ. </li>
    </ul>
    <h4>&#10140; Cần xử lý sự mất cân bằng để đảm bảo mô hình không bị bias.</h4>
        </div>
    """,
    unsafe_allow_html=True,
)
image_path_phan_phoi_so_lieu = os.path.join(current_dir, "phan_phoi_so_lieu.jpg")
st.image(image_path_phan_phoi_so_lieu, use_container_width=True)

st.markdown(
    """
     <p style:"text-align: center;"><i>Hình: Phân phối số sao và Phân phối sentiment (dựa trên số sao)</i></p>
     <h5>Xem phân phối độ dài bình luận:</h5>
    <ul>
    <li>Phương án: áp dụng Log Transform để phân phối độ dài bình luận trở nên cân đối hơn</li>
    </ul>
         """,
    unsafe_allow_html=True,
)
image_path_Log_Comment_Length = os.path.join(current_dir, "Log_Comment_Length.png")
st.image(image_path_Log_Comment_Length, use_container_width=True)

st.markdown(
    """
    <p style:"text-align: center;"><i>Hình: Trước và sau khi áp dụng Log Transform</i></p>
    </div>
    """,
    unsafe_allow_html=True,
)

# Data Preparation
# Đường dẫn tuyệt đối đến thư mục chứa hình ảnh
current_dir = os.path.dirname(os.path.abspath(__file__))
image_path = os.path.join(current_dir, "logo.jpg")

sidebarlogo = Image.open('logo.jpg').resize((100, 50))
# Tạo tiêu đề
st.markdown(
    """
    <div class="container">
        <div class="header">
            <h1>Data Preparation</h1>
            <hr>
        </div>
        <div class="sub-header">
        <ul>
        <li>Xử lý dữ liệu văn bản</li>
        <li>Chuẩn bị dữ liệu đầu vào cho mô hình học máy</li>
        </ul>
        </div>
        <div class="content">
    """,
    unsafe_allow_html=True,
)
st.markdown(
    """
    <h3>Xử lý dữ liệu văn bản:</h3>
       """,
    unsafe_allow_html=True,
)
image_text_processing_flow = os.path.join(current_dir, "text_processing_flow.jpg")
st.image(image_text_processing_flow, use_container_width=False)

st.markdown(
    """
    <p style:"text-align: center;"><i>Hình: FlowChart xử lý dữ liệu văn bản.</i></p>
    """,
    unsafe_allow_html=True,)
# Tạo bảng so sánh trước và sau xử lý beforeAfter_TextProcessing
image_beforeAfter_TextProcessing = os.path.join(current_dir, "beforeAfter_TextProcessing.jpg")
st.image(image_beforeAfter_TextProcessing, use_container_width=False)
st.markdown(
    """
    <p style:"text-align: center;"><i>Hình: Cột Noi_dung_binh_luan trước và sau khi xử lý dữ liệu.</i></p>
    """,
    unsafe_allow_html=True,)

st.markdown("""<h4>Tạo thêm các cột mới dựa trên việc đếm từ/icon positive, negative, neutral:</h4> """,unsafe_allow_html=True,)
image_GenerateNewColumn= os.path.join(current_dir, "GenerateNewColumn.jpg")
st.image(image_GenerateNewColumn, use_container_width=False)
st.markdown("""<p style:"text-align: center;"><i>Hình: Hiển thị thêm 3 cột mới sau khi đếm.</i></p> """, unsafe_allow_html=True,)

st.markdown("""<h4>Kiểm tra Word Cloud:</h4> """,unsafe_allow_html=True,)
image_wordCloud= os.path.join(current_dir, "wordCloud.png")
st.image(image_wordCloud, use_container_width=False)
st.markdown("""<p style:"text-align: center;"><i>Hình: Hiển thị Word Cloud Positive-Neutral-Negative words.</i></p> """, unsafe_allow_html=True,)

st.markdown("""<h4>Thống Kê Số Lượng Từ Theo Sentiment:</h4> """,unsafe_allow_html=True,)
image_ThongKe= os.path.join(current_dir, "ThongKe.JPG")
st.image(image_ThongKe, use_container_width=False)

image_ThongKeChart= os.path.join(current_dir, "ThongKeChart.JPG")
st.image(image_ThongKeChart, use_container_width=False)
st.markdown("""<p style:"text-align: center;"><i>Hình: Tổng số lượng từ tích cực, tiêu cực, trung tính theo sentiment.</i></p> """, unsafe_allow_html=True,)

st.markdown("""<h3>Chuẩn bị dữ liệu đầu vào cho mô hình học máy:</h3> """,unsafe_allow_html=True,)
st.markdown("""
    <ul>
    <li>CountVectorizer.</li>
    <li>TF-IDF Vectorizer.</li>
    <li>Tách dữ liệu thành tập huấn luyện và kiểm thử (80:20).</li>
    <li>Xử lý mất cân bằng dữ liệu bằng SMOTE chỉ trên tập train.</li>
    </ul>   """,
    unsafe_allow_html=True,)

image_Smote= os.path.join(current_dir, "Smote.JPG")
st.image(image_Smote, use_container_width=False)
st.markdown("""<p style:"text-align: center;"><i>Hình: Trước và sau khi áp dụng SMOTE.</i></p> """, unsafe_allow_html=True,)
st.markdown("""</div></div>""", unsafe_allow_html=True,)




# Tạo tiêu đề Modeling & Evaluation (for ML & Big data)
st.markdown(
    """
    <div class="container">
        <div class="header">
            <h1>Modeling & Evaluation (for ML & Big data)</h1>
            <hr>
        </div>
        <div class="sub-header">
            Tổng quan về BData Understanding:
        </div>
        <div class="content">
    """,
    unsafe_allow_html=True,
)
 
st.markdown(
    """
    <h3>Dữ liệu cung cấp:</h3>
    <ul>
    <li>San_pham.csv: Thông tin về sản phẩm.</li>
    <li>Khach_hang.csv: Thông tin về khách hàng.</li>
    <li>Danh_gia.csv: Chứa các đánh giá của khách hàng.</li>
    </ul>
    <h3>Dữ liệu trọng tâm:</h3>
    <ul><li>Bài toán sentiment analysis tập trung vào hai cột chính trong tệp Danh_gia.csv.</li></ul>
     """,
    unsafe_allow_html=True,
)











# Tiêu đề biểu đồ

st.markdown( """<div class="chart-title">App & developer growth</div><hr style="border: 1px solid #00d7ff;">""",unsafe_allow_html=True,)

# Dữ liệu mẫu
week_start = [
    "Apr 16", "Apr 23", "Apr 30", "May 07", "May 14", "May 21", "May 28", "Jun 04", "Jun 11",
    "Jun 18", "Jun 25", "Jul 02", "Jul 09", "Jul 16", "Jul 23", "Jul 30", "Aug 06", "Aug 13",
    "Aug 20", "Aug 27", "Sep 03", "Sep 10", "Sep 17", "Sep 24", "Oct 01", "Oct 08", "Oct 15",
    "Oct 22", "Oct 29", "Nov 05", "Nov 12", "Nov 19", "Nov 26", "Dec 03", "Dec 10", "Dec 17",
    "Dec 24", "Dec 31"
]

apps_created = [
    500, 700, 900, 1200, 1400, 1600, 1800, 2000, 2200, 2500, 2800, 3100, 3400, 3700, 4000, 4300,
    4600, 4900, 5100, 5300, 5600, 5800, 6000, 6200, 6400, 6700, 6900, 7100, 7400, 7700, 8000,
    8200, 8500, 8800, 9000, 9100, 9200
]

unique_developers = [
    400, 600, 800, 1000, 1200, 1400, 1600, 1800, 2000, 2200, 2400, 2600, 2800, 3000, 3200, 3400,
    3600, 3800, 4000, 4200, 4400, 4600, 4800, 5000, 5200, 5400, 5600, 5800, 6000, 6200, 6400,
    6600, 6800, 7000, 7200, 7400, 7600
]

# Tạo biểu đồ với Plotly
fig = go.Figure()
fig.add_trace(go.Scatter(x=week_start, y=apps_created, mode='lines+markers', name='Apps created',
                         line=dict(color='#00d7ff', width=2)))
fig.add_trace(go.Scatter(x=week_start, y=unique_developers, mode='lines+markers', name='Unique developers',
                         line=dict(color='#ffaa00', width=2)))

# Tùy chỉnh giao diện biểu đồ
fig.update_layout(
    title="",
    xaxis_title="Week Start",
    yaxis_title="Weekly Count",
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    plot_bgcolor='#1a1a1a',
    paper_bgcolor='#1a1a1a',
    font=dict(color="white"),
    margin=dict(l=40, r=40, t=40, b=40)
)

# Hiển thị biểu đồ
st.plotly_chart(fig, use_container_width=True)

# Nội dung nhận xét
st.markdown(
    """
    <div class="content">
        <p>
            <span class="highlight">17,926 unique developers</span> đã tạo tổng cộng <span class="highlight">29,183 apps</span>.
        </p>
        <p>
            Trung bình, mỗi nhà phát triển đã tạo <span class="highlight">1.6 apps</span>. 
        </p>
        <p>
            Các ứng dụng này sử dụng sức mạnh của LLMs để xử lý nhiều tác vụ NLP, bao gồm:
        </p>
        <ul>
            <li>Content generation</li>
            <li>Language translation</li>
            <li>Chatbots and virtual assistants</li>
            <li>Data analysis and insights</li>
            <li>Content summarization</li>
        </ul>
    </div>
    """,
    unsafe_allow_html=True,
)

