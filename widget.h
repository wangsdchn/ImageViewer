#ifndef WIDGET_H
#define WIDGET_H

#include <QWidget>
#include <QPushButton>
#include <QLabel>
#include <QGridLayout>
#include <QPixmap>
#include <QWheelEvent>
#include <QImageReader>
#include <QImage>

class Widget : public QWidget
{
    Q_OBJECT

public:
    Widget(QWidget *parent = 0);
    ~Widget();
    void showPicture(float scale = 1.0);
private slots:
    void wheelEvent(QWheelEvent * event);
private:
    QPushButton *ReadImgBtn;
    QLabel *ShowImgLabel;
    float Scale;
    QPixmap Image;
    QGridLayout *MainGridLayout;
};

#endif // WIDGET_H
