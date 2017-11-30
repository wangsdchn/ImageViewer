#include "widget.h"

Widget::Widget(QWidget *parent)
    : QWidget(parent)
{
    resize(QSize(640,480));
    Scale = 1.0;

    QString path="E:/wsd/index.jpg";
    QImageReader reader;
    reader.setFileName(path);
    QSize imageSize = reader.size();
    imageSize.scale(size(), Qt::KeepAspectRatio);
    reader.setScaledSize(imageSize);
    QImage image = reader.read();
    // Make QPixmap (if needed)


    //Image = new QPixmap;
    Image = QPixmap::fromImage(image);

    ReadImgBtn = new QPushButton(tr("Read An Image"));
    ShowImgLabel = new QLabel(tr("image"));
    ShowImgLabel->setAlignment(Qt::AlignCenter);
    ShowImgLabel->setFixedSize(800, 600);

    MainGridLayout = new QGridLayout(this);
    MainGridLayout->addWidget(ReadImgBtn,0,0);
    MainGridLayout->addWidget(ShowImgLabel,0,1);
}
void Widget::wheelEvent(QWheelEvent *event)
{

    int numDegress = event->delta();
    if (numDegress > 0)
        Scale *= 1.2;
    else
        Scale /= 1.2;

    showPicture(Scale);
}
void Widget::showPicture(float scale)
{
    ShowImgLabel->setPixmap(Image.scaled(
                            800*scale, 600*scale,
                            Qt::KeepAspectRatio));
}
Widget::~Widget()
{

}
