/****************************************************************************
** Meta object code from reading C++ file 'FileTinderDialog.hpp'
**
** Created by: The Qt Meta Object Compiler version 68 (Qt 6.4.2)
**
** WARNING! All changes made in this file will be lost!
*****************************************************************************/

#include <memory>
#include "../../../app/include/FileTinderDialog.hpp"
#include <QtGui/qtextcursor.h>
#include <QtCore/qmetatype.h>
#if !defined(Q_MOC_OUTPUT_REVISION)
#error "The header file 'FileTinderDialog.hpp' doesn't include <QObject>."
#elif Q_MOC_OUTPUT_REVISION != 68
#error "This file was generated using the moc from 6.4.2. It"
#error "cannot be used with the include files from this version of Qt."
#error "(The moc has changed too much.)"
#endif

#ifndef Q_CONSTINIT
#define Q_CONSTINIT
#endif

QT_BEGIN_MOC_NAMESPACE
QT_WARNING_PUSH
QT_WARNING_DISABLE_DEPRECATED
namespace {
struct qt_meta_stringdata_FileTinderDialog_t {
    uint offsetsAndSizes[16];
    char stringdata0[17];
    char stringdata1[13];
    char stringdata2[1];
    char stringdata3[15];
    char stringdata4[15];
    char stringdata5[19];
    char stringdata6[17];
    char stringdata7[21];
};
#define QT_MOC_LITERAL(ofs, len) \
    uint(sizeof(qt_meta_stringdata_FileTinderDialog_t::offsetsAndSizes) + ofs), len 
Q_CONSTINIT static const qt_meta_stringdata_FileTinderDialog_t qt_meta_stringdata_FileTinderDialog = {
    {
        QT_MOC_LITERAL(0, 16),  // "FileTinderDialog"
        QT_MOC_LITERAL(17, 12),  // "on_keep_file"
        QT_MOC_LITERAL(30, 0),  // ""
        QT_MOC_LITERAL(31, 14),  // "on_delete_file"
        QT_MOC_LITERAL(46, 14),  // "on_ignore_file"
        QT_MOC_LITERAL(61, 18),  // "on_revert_decision"
        QT_MOC_LITERAL(80, 16),  // "on_finish_review"
        QT_MOC_LITERAL(97, 20)   // "on_execute_deletions"
    },
    "FileTinderDialog",
    "on_keep_file",
    "",
    "on_delete_file",
    "on_ignore_file",
    "on_revert_decision",
    "on_finish_review",
    "on_execute_deletions"
};
#undef QT_MOC_LITERAL
} // unnamed namespace

Q_CONSTINIT static const uint qt_meta_data_FileTinderDialog[] = {

 // content:
      10,       // revision
       0,       // classname
       0,    0, // classinfo
       6,   14, // methods
       0,    0, // properties
       0,    0, // enums/sets
       0,    0, // constructors
       0,       // flags
       0,       // signalCount

 // slots: name, argc, parameters, tag, flags, initial metatype offsets
       1,    0,   50,    2, 0x08,    1 /* Private */,
       3,    0,   51,    2, 0x08,    2 /* Private */,
       4,    0,   52,    2, 0x08,    3 /* Private */,
       5,    0,   53,    2, 0x08,    4 /* Private */,
       6,    0,   54,    2, 0x08,    5 /* Private */,
       7,    0,   55,    2, 0x08,    6 /* Private */,

 // slots: parameters
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,

       0        // eod
};

Q_CONSTINIT const QMetaObject FileTinderDialog::staticMetaObject = { {
    QMetaObject::SuperData::link<QDialog::staticMetaObject>(),
    qt_meta_stringdata_FileTinderDialog.offsetsAndSizes,
    qt_meta_data_FileTinderDialog,
    qt_static_metacall,
    nullptr,
    qt_incomplete_metaTypeArray<qt_meta_stringdata_FileTinderDialog_t,
        // Q_OBJECT / Q_GADGET
        QtPrivate::TypeAndForceComplete<FileTinderDialog, std::true_type>,
        // method 'on_keep_file'
        QtPrivate::TypeAndForceComplete<void, std::false_type>,
        // method 'on_delete_file'
        QtPrivate::TypeAndForceComplete<void, std::false_type>,
        // method 'on_ignore_file'
        QtPrivate::TypeAndForceComplete<void, std::false_type>,
        // method 'on_revert_decision'
        QtPrivate::TypeAndForceComplete<void, std::false_type>,
        // method 'on_finish_review'
        QtPrivate::TypeAndForceComplete<void, std::false_type>,
        // method 'on_execute_deletions'
        QtPrivate::TypeAndForceComplete<void, std::false_type>
    >,
    nullptr
} };

void FileTinderDialog::qt_static_metacall(QObject *_o, QMetaObject::Call _c, int _id, void **_a)
{
    if (_c == QMetaObject::InvokeMetaMethod) {
        auto *_t = static_cast<FileTinderDialog *>(_o);
        (void)_t;
        switch (_id) {
        case 0: _t->on_keep_file(); break;
        case 1: _t->on_delete_file(); break;
        case 2: _t->on_ignore_file(); break;
        case 3: _t->on_revert_decision(); break;
        case 4: _t->on_finish_review(); break;
        case 5: _t->on_execute_deletions(); break;
        default: ;
        }
    }
    (void)_a;
}

const QMetaObject *FileTinderDialog::metaObject() const
{
    return QObject::d_ptr->metaObject ? QObject::d_ptr->dynamicMetaObject() : &staticMetaObject;
}

void *FileTinderDialog::qt_metacast(const char *_clname)
{
    if (!_clname) return nullptr;
    if (!strcmp(_clname, qt_meta_stringdata_FileTinderDialog.stringdata0))
        return static_cast<void*>(this);
    return QDialog::qt_metacast(_clname);
}

int FileTinderDialog::qt_metacall(QMetaObject::Call _c, int _id, void **_a)
{
    _id = QDialog::qt_metacall(_c, _id, _a);
    if (_id < 0)
        return _id;
    if (_c == QMetaObject::InvokeMetaMethod) {
        if (_id < 6)
            qt_static_metacall(this, _c, _id, _a);
        _id -= 6;
    } else if (_c == QMetaObject::RegisterMethodArgumentMetaType) {
        if (_id < 6)
            *reinterpret_cast<QMetaType *>(_a[0]) = QMetaType();
        _id -= 6;
    }
    return _id;
}
QT_WARNING_POP
QT_END_MOC_NAMESPACE
