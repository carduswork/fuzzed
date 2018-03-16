// Copyright (c) 2005-2014 Code Synthesis Tools CC
//
// This program was generated by CodeSynthesis XSD, an XML Schema to
// C++ data binding compiler.
//
// This program is free software; you can redistribute it and/or modify
// it under the terms of the GNU General Public License version 2 as
// published by the Free Software Foundation.
//
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with this program; if not, write to the Free Software
// Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301 USA
//
// In addition, as a special exception, Code Synthesis Tools CC gives
// permission to link this program with the Xerces-C++ library (or with
// modified versions of Xerces-C++ that use the same license as Xerces-C++),
// and distribute linked combinations including the two. You must obey
// the GNU General Public License version 2 in all respects for all of
// the code used other than Xerces-C++. If you modify this copy of the
// program, you may extend this exception to your version of the program,
// but you are not obligated to do so. If you do not wish to do so, delete
// this exception statement from your version.
//
// Furthermore, Code Synthesis Tools CC makes a special exception for
// the Free/Libre and Open Source Software (FLOSS) which is described
// in the accompanying FLOSSE file.
//

#ifndef CXX_ORE_BACK____FRONT_FUZZ_ED_STATIC_XSD_COMMON_H
#define CXX_ORE_BACK____FRONT_FUZZ_ED_STATIC_XSD_COMMON_H

#ifndef XSD_USE_CHAR
#define XSD_USE_CHAR
#endif

#ifndef XSD_CXX_TREE_USE_CHAR
#define XSD_CXX_TREE_USE_CHAR
#endif

// Begin prologue.
//
//
// End prologue.

#include <xsd/cxx/config.hxx>

#if (XSD_INT_VERSION != 4000000L)
#error XSD runtime version mismatch
#endif

#include <xsd/cxx/pre.hxx>

#include <xsd/cxx/xml/char-utf8.hxx>

#include <xsd/cxx/tree/exceptions.hxx>
#include <xsd/cxx/tree/elements.hxx>
#include <xsd/cxx/tree/types.hxx>

#include <xsd/cxx/xml/error-handler.hxx>

#include <xsd/cxx/xml/dom/auto-ptr.hxx>

#include <xsd/cxx/tree/parsing.hxx>
#include <xsd/cxx/tree/parsing/byte.hxx>
#include <xsd/cxx/tree/parsing/unsigned-byte.hxx>
#include <xsd/cxx/tree/parsing/short.hxx>
#include <xsd/cxx/tree/parsing/unsigned-short.hxx>
#include <xsd/cxx/tree/parsing/int.hxx>
#include <xsd/cxx/tree/parsing/unsigned-int.hxx>
#include <xsd/cxx/tree/parsing/long.hxx>
#include <xsd/cxx/tree/parsing/unsigned-long.hxx>
#include <xsd/cxx/tree/parsing/boolean.hxx>
#include <xsd/cxx/tree/parsing/float.hxx>
#include <xsd/cxx/tree/parsing/double.hxx>
#include <xsd/cxx/tree/parsing/decimal.hxx>

#include <xsd/cxx/xml/dom/serialization-header.hxx>
#include <xsd/cxx/tree/serialization.hxx>
#include <xsd/cxx/tree/serialization/byte.hxx>
#include <xsd/cxx/tree/serialization/unsigned-byte.hxx>
#include <xsd/cxx/tree/serialization/short.hxx>
#include <xsd/cxx/tree/serialization/unsigned-short.hxx>
#include <xsd/cxx/tree/serialization/int.hxx>
#include <xsd/cxx/tree/serialization/unsigned-int.hxx>
#include <xsd/cxx/tree/serialization/long.hxx>
#include <xsd/cxx/tree/serialization/unsigned-long.hxx>
#include <xsd/cxx/tree/serialization/boolean.hxx>
#include <xsd/cxx/tree/serialization/float.hxx>
#include <xsd/cxx/tree/serialization/double.hxx>
#include <xsd/cxx/tree/serialization/decimal.hxx>

namespace xml_schema
{
  // anyType and anySimpleType.
  //
  typedef ::xsd::cxx::tree::type Type;
  typedef ::xsd::cxx::tree::simple_type< char, Type > SimpleType;
  typedef ::xsd::cxx::tree::type Container;

  // 8-bit
  //
  typedef signed char Byte;
  typedef unsigned char UnsignedByte;

  // 16-bit
  //
  typedef short Short;
  typedef unsigned short UnsignedShort;

  // 32-bit
  //
  typedef int Int;
  typedef unsigned int UnsignedInt;

  // 64-bit
  //
  typedef long long Long;
  typedef unsigned long long UnsignedLong;

  // Supposed to be arbitrary-length integral types.
  //
  typedef long long Integer;
  typedef long long NonPositiveInteger;
  typedef unsigned long long NonNegativeInteger;
  typedef unsigned long long PositiveInteger;
  typedef long long NegativeInteger;

  // Boolean.
  //
  typedef bool Boolean;

  // Floating-point types.
  //
  typedef float Float;
  typedef double Double;
  typedef double Decimal;

  // String types.
  //
  typedef ::xsd::cxx::tree::string< char, SimpleType > String;
  typedef ::xsd::cxx::tree::normalized_string< char, String > NormalizedString;
  typedef ::xsd::cxx::tree::token< char, NormalizedString > Token;
  typedef ::xsd::cxx::tree::name< char, Token > Name;
  typedef ::xsd::cxx::tree::nmtoken< char, Token > Nmtoken;
  typedef ::xsd::cxx::tree::nmtokens< char, SimpleType, Nmtoken > Nmtokens;
  typedef ::xsd::cxx::tree::ncname< char, Name > Ncname;
  typedef ::xsd::cxx::tree::language< char, Token > Language;

  // ID/IDREF.
  //
  typedef ::xsd::cxx::tree::id< char, Ncname > Id;
  typedef ::xsd::cxx::tree::idref< char, Ncname, Type > Idref;
  typedef ::xsd::cxx::tree::idrefs< char, SimpleType, Idref > Idrefs;

  // URI.
  //
  typedef ::xsd::cxx::tree::uri< char, SimpleType > Uri;

  // Qualified name.
  //
  typedef ::xsd::cxx::tree::qname< char, SimpleType, Uri, Ncname > Qname;

  // Binary.
  //
  typedef ::xsd::cxx::tree::buffer< char > Buffer;
  typedef ::xsd::cxx::tree::base64_binary< char, SimpleType > Base64Binary;
  typedef ::xsd::cxx::tree::hex_binary< char, SimpleType > HexBinary;

  // Date/time.
  //
  typedef ::xsd::cxx::tree::time_zone TimeZone;
  typedef ::xsd::cxx::tree::date< char, SimpleType > Date;
  typedef ::xsd::cxx::tree::date_time< char, SimpleType > DateTime;
  typedef ::xsd::cxx::tree::duration< char, SimpleType > Duration;
  typedef ::xsd::cxx::tree::gday< char, SimpleType > Gday;
  typedef ::xsd::cxx::tree::gmonth< char, SimpleType > Gmonth;
  typedef ::xsd::cxx::tree::gmonth_day< char, SimpleType > GmonthDay;
  typedef ::xsd::cxx::tree::gyear< char, SimpleType > Gyear;
  typedef ::xsd::cxx::tree::gyear_month< char, SimpleType > GyearMonth;
  typedef ::xsd::cxx::tree::time< char, SimpleType > Time;

  // Entity.
  //
  typedef ::xsd::cxx::tree::entity< char, Ncname > Entity;
  typedef ::xsd::cxx::tree::entities< char, SimpleType, Entity > Entities;

  typedef ::xsd::cxx::tree::content_order ContentOrder;
  // Namespace information and list stream. Used in
  // serialization functions.
  //
  typedef ::xsd::cxx::xml::dom::namespace_info< char > NamespaceInfo;
  typedef ::xsd::cxx::xml::dom::namespace_infomap< char > NamespaceInfomap;
  typedef ::xsd::cxx::tree::list_stream< char > ListStream;
  typedef ::xsd::cxx::tree::as_double< Double > AsDouble;
  typedef ::xsd::cxx::tree::as_decimal< Decimal > AsDecimal;
  typedef ::xsd::cxx::tree::facet Facet;

  // Flags and properties.
  //
  typedef ::xsd::cxx::tree::flags Flags;
  typedef ::xsd::cxx::tree::properties< char > Properties;

  // Parsing/serialization diagnostics.
  //
  typedef ::xsd::cxx::tree::severity Severity;
  typedef ::xsd::cxx::tree::error< char > Error;
  typedef ::xsd::cxx::tree::diagnostics< char > Diagnostics;

  // Exceptions.
  //
  typedef ::xsd::cxx::tree::exception< char > Exception;
  typedef ::xsd::cxx::tree::bounds< char > Bounds;
  typedef ::xsd::cxx::tree::duplicate_id< char > DuplicateId;
  typedef ::xsd::cxx::tree::parsing< char > Parsing;
  typedef ::xsd::cxx::tree::expected_element< char > ExpectedElement;
  typedef ::xsd::cxx::tree::unexpected_element< char > UnexpectedElement;
  typedef ::xsd::cxx::tree::expected_attribute< char > ExpectedAttribute;
  typedef ::xsd::cxx::tree::unexpected_enumerator< char > UnexpectedEnumerator;
  typedef ::xsd::cxx::tree::expected_text_content< char > ExpectedTextContent;
  typedef ::xsd::cxx::tree::no_prefix_mapping< char > NoPrefixMapping;
  typedef ::xsd::cxx::tree::no_type_info< char > NoTypeInfo;
  typedef ::xsd::cxx::tree::not_derived< char > NotDerived;
  typedef ::xsd::cxx::tree::serialization< char > Serialization;

  // Error handler callback interface.
  //
  typedef ::xsd::cxx::xml::error_handler< char > ErrorHandler;

  // DOM interaction.
  //
  namespace dom
  {
    // Automatic pointer for DOMDocument.
    //
    using ::xsd::cxx::xml::dom::auto_ptr;

#ifndef XSD_CXX_TREE_TREE_NODE_KEY__XML_SCHEMA
#define XSD_CXX_TREE_TREE_NODE_KEY__XML_SCHEMA
    // DOM user data key for back pointers to tree nodes.
    //
    const XMLCh* const treeNodeKey = ::xsd::cxx::tree::user_data_keys::node;
#endif
  }
}

// Forward declarations.
//
namespace commonTypes
{
  class Model;
  class GraphNode;
  class IdList;
  class DoubleToIntervalMap;
  class Interval;
  class Issue;
  class Probability;
  class CrispProbability;
  class DecomposedFuzzyProbability;
}


#include <memory>    // ::std::auto_ptr
#include <limits>    // std::numeric_limits
#include <algorithm> // std::binary_search

#include <xsd/cxx/xml/char-utf8.hxx>

#include <xsd/cxx/tree/exceptions.hxx>
#include <xsd/cxx/tree/elements.hxx>
#include <xsd/cxx/tree/containers.hxx>
#include <xsd/cxx/tree/list.hxx>

#include <xsd/cxx/xml/dom/parsing-header.hxx>

namespace commonTypes
{
  class Model: public ::xml_schema::Type
  {
    public:
    // id
    //
    typedef ::xml_schema::String IdType;
    typedef ::xsd::cxx::tree::optional< IdType > IdOptional;
    typedef ::xsd::cxx::tree::traits< IdType, char > IdTraits;

    const IdOptional&
    id () const;

    IdOptional&
    id ();

    void
    id (const IdType& x);

    void
    id (const IdOptional& x);

    void
    id (::std::auto_ptr< IdType > p);

    // Constructors.
    //
    Model ();

    Model (const ::xercesc::DOMElement& e,
           ::xml_schema::Flags f = 0,
           ::xml_schema::Container* c = 0);

    Model (const Model& x,
           ::xml_schema::Flags f = 0,
           ::xml_schema::Container* c = 0);

    virtual Model*
    _clone (::xml_schema::Flags f = 0,
            ::xml_schema::Container* c = 0) const;

    Model&
    operator= (const Model& x);

    virtual 
    ~Model ();

    // Implementation.
    //
    protected:
    void
    parse (::xsd::cxx::xml::dom::parser< char >&,
           ::xml_schema::Flags);

    protected:
    IdOptional id_;
  };

  class GraphNode: public ::xml_schema::Type
  {
    public:
    // x
    //
    typedef ::xml_schema::Int XType;
    typedef ::xsd::cxx::tree::optional< XType > XOptional;
    typedef ::xsd::cxx::tree::traits< XType, char > XTraits;

    const XOptional&
    x () const;

    XOptional&
    x ();

    void
    x (const XType& x);

    void
    x (const XOptional& x);

    // y
    //
    typedef ::xml_schema::Int YType;
    typedef ::xsd::cxx::tree::optional< YType > YOptional;
    typedef ::xsd::cxx::tree::traits< YType, char > YTraits;

    const YOptional&
    y () const;

    YOptional&
    y ();

    void
    y (const YType& x);

    void
    y (const YOptional& x);

    // id
    //
    typedef ::xml_schema::String IdType;
    typedef ::xsd::cxx::tree::optional< IdType > IdOptional;
    typedef ::xsd::cxx::tree::traits< IdType, char > IdTraits;

    const IdOptional&
    id () const;

    IdOptional&
    id ();

    void
    id (const IdType& x);

    void
    id (const IdOptional& x);

    void
    id (::std::auto_ptr< IdType > p);

    // Constructors.
    //
    GraphNode ();

    GraphNode (const ::xercesc::DOMElement& e,
               ::xml_schema::Flags f = 0,
               ::xml_schema::Container* c = 0);

    GraphNode (const GraphNode& x,
               ::xml_schema::Flags f = 0,
               ::xml_schema::Container* c = 0);

    virtual GraphNode*
    _clone (::xml_schema::Flags f = 0,
            ::xml_schema::Container* c = 0) const;

    GraphNode&
    operator= (const GraphNode& x);

    virtual 
    ~GraphNode ();

    // Implementation.
    //
    protected:
    void
    parse (::xsd::cxx::xml::dom::parser< char >&,
           ::xml_schema::Flags);

    protected:
    XOptional x_;
    YOptional y_;
    IdOptional id_;
  };

  class IdList: public ::xml_schema::SimpleType,
    public ::xsd::cxx::tree::list< ::xml_schema::String, char >
  {
    public:
    IdList ();

    IdList (size_type n, const ::xml_schema::String& x);

    template < typename I >
    IdList (const I& begin, const I& end)
    : ::xsd::cxx::tree::list< ::xml_schema::String, char > (begin, end, this)
    {
    }

    IdList (const ::xercesc::DOMElement& e,
            ::xml_schema::Flags f = 0,
            ::xml_schema::Container* c = 0);

    IdList (const ::xercesc::DOMAttr& a,
            ::xml_schema::Flags f = 0,
            ::xml_schema::Container* c = 0);

    IdList (const ::std::string& s,
            const ::xercesc::DOMElement* e,
            ::xml_schema::Flags f = 0,
            ::xml_schema::Container* c = 0);

    IdList (const IdList& x,
            ::xml_schema::Flags f = 0,
            ::xml_schema::Container* c = 0);

    virtual IdList*
    _clone (::xml_schema::Flags f = 0,
            ::xml_schema::Container* c = 0) const;

    virtual 
    ~IdList ();
  };

  class DoubleToIntervalMap: public ::xml_schema::Type
  {
    public:
    // value
    //
    typedef ::commonTypes::Interval ValueType;
    typedef ::xsd::cxx::tree::traits< ValueType, char > ValueTraits;

    const ValueType&
    value () const;

    ValueType&
    value ();

    void
    value (const ValueType& x);

    void
    value (::std::auto_ptr< ValueType > p);

    // key
    //
    typedef ::xml_schema::Double KeyType;
    typedef ::xsd::cxx::tree::traits< KeyType, char, ::xsd::cxx::tree::schema_type::double_ > KeyTraits;

    const KeyType&
    key () const;

    KeyType&
    key ();

    void
    key (const KeyType& x);

    // Constructors.
    //
    DoubleToIntervalMap (const ValueType&,
                         const KeyType&);

    DoubleToIntervalMap (::std::auto_ptr< ValueType >,
                         const KeyType&);

    DoubleToIntervalMap (const ::xercesc::DOMElement& e,
                         ::xml_schema::Flags f = 0,
                         ::xml_schema::Container* c = 0);

    DoubleToIntervalMap (const DoubleToIntervalMap& x,
                         ::xml_schema::Flags f = 0,
                         ::xml_schema::Container* c = 0);

    virtual DoubleToIntervalMap*
    _clone (::xml_schema::Flags f = 0,
            ::xml_schema::Container* c = 0) const;

    DoubleToIntervalMap&
    operator= (const DoubleToIntervalMap& x);

    virtual 
    ~DoubleToIntervalMap ();

    // Implementation.
    //
    protected:
    void
    parse (::xsd::cxx::xml::dom::parser< char >&,
           ::xml_schema::Flags);

    protected:
    ::xsd::cxx::tree::one< ValueType > value_;
    ::xsd::cxx::tree::one< KeyType > key_;
  };

  class Interval: public ::xml_schema::Type
  {
    public:
    // lowerBound
    //
    typedef ::xml_schema::Double LowerBoundType;
    typedef ::xsd::cxx::tree::traits< LowerBoundType, char, ::xsd::cxx::tree::schema_type::double_ > LowerBoundTraits;

    const LowerBoundType&
    lowerBound () const;

    LowerBoundType&
    lowerBound ();

    void
    lowerBound (const LowerBoundType& x);

    // upperBound
    //
    typedef ::xml_schema::Double UpperBoundType;
    typedef ::xsd::cxx::tree::traits< UpperBoundType, char, ::xsd::cxx::tree::schema_type::double_ > UpperBoundTraits;

    const UpperBoundType&
    upperBound () const;

    UpperBoundType&
    upperBound ();

    void
    upperBound (const UpperBoundType& x);

    // Constructors.
    //
    Interval (const LowerBoundType&,
              const UpperBoundType&);

    Interval (const ::xercesc::DOMElement& e,
              ::xml_schema::Flags f = 0,
              ::xml_schema::Container* c = 0);

    Interval (const Interval& x,
              ::xml_schema::Flags f = 0,
              ::xml_schema::Container* c = 0);

    virtual Interval*
    _clone (::xml_schema::Flags f = 0,
            ::xml_schema::Container* c = 0) const;

    Interval&
    operator= (const Interval& x);

    virtual 
    ~Interval ();

    // Implementation.
    //
    protected:
    void
    parse (::xsd::cxx::xml::dom::parser< char >&,
           ::xml_schema::Flags);

    protected:
    ::xsd::cxx::tree::one< LowerBoundType > lowerBound_;
    ::xsd::cxx::tree::one< UpperBoundType > upperBound_;
  };

  class Issue: public ::xml_schema::Type
  {
    public:
    // issueId
    //
    typedef ::xml_schema::Int IssueIdType;
    typedef ::xsd::cxx::tree::optional< IssueIdType > IssueIdOptional;
    typedef ::xsd::cxx::tree::traits< IssueIdType, char > IssueIdTraits;

    const IssueIdOptional&
    issueId () const;

    IssueIdOptional&
    issueId ();

    void
    issueId (const IssueIdType& x);

    void
    issueId (const IssueIdOptional& x);

    // elementId
    //
    typedef ::xml_schema::String ElementIdType;
    typedef ::xsd::cxx::tree::optional< ElementIdType > ElementIdOptional;
    typedef ::xsd::cxx::tree::traits< ElementIdType, char > ElementIdTraits;

    const ElementIdOptional&
    elementId () const;

    ElementIdOptional&
    elementId ();

    void
    elementId (const ElementIdType& x);

    void
    elementId (const ElementIdOptional& x);

    void
    elementId (::std::auto_ptr< ElementIdType > p);

    // message
    //
    typedef ::xml_schema::String MessageType;
    typedef ::xsd::cxx::tree::optional< MessageType > MessageOptional;
    typedef ::xsd::cxx::tree::traits< MessageType, char > MessageTraits;

    const MessageOptional&
    message () const;

    MessageOptional&
    message ();

    void
    message (const MessageType& x);

    void
    message (const MessageOptional& x);

    void
    message (::std::auto_ptr< MessageType > p);

    // isFatal
    //
    typedef ::xml_schema::Boolean IsFatalType;
    typedef ::xsd::cxx::tree::optional< IsFatalType > IsFatalOptional;
    typedef ::xsd::cxx::tree::traits< IsFatalType, char > IsFatalTraits;

    const IsFatalOptional&
    isFatal () const;

    IsFatalOptional&
    isFatal ();

    void
    isFatal (const IsFatalType& x);

    void
    isFatal (const IsFatalOptional& x);

    // Constructors.
    //
    Issue ();

    Issue (const ::xercesc::DOMElement& e,
           ::xml_schema::Flags f = 0,
           ::xml_schema::Container* c = 0);

    Issue (const Issue& x,
           ::xml_schema::Flags f = 0,
           ::xml_schema::Container* c = 0);

    virtual Issue*
    _clone (::xml_schema::Flags f = 0,
            ::xml_schema::Container* c = 0) const;

    Issue&
    operator= (const Issue& x);

    virtual 
    ~Issue ();

    // Implementation.
    //
    protected:
    void
    parse (::xsd::cxx::xml::dom::parser< char >&,
           ::xml_schema::Flags);

    protected:
    IssueIdOptional issueId_;
    ElementIdOptional elementId_;
    MessageOptional message_;
    IsFatalOptional isFatal_;
  };

  class Probability: public ::xml_schema::Type
  {
    public:
    // Constructors.
    //
    Probability ();

    Probability (const ::xercesc::DOMElement& e,
                 ::xml_schema::Flags f = 0,
                 ::xml_schema::Container* c = 0);

    Probability (const ::xercesc::DOMAttr& a,
                 ::xml_schema::Flags f = 0,
                 ::xml_schema::Container* c = 0);

    Probability (const ::std::string& s,
                 const ::xercesc::DOMElement* e,
                 ::xml_schema::Flags f = 0,
                 ::xml_schema::Container* c = 0);

    Probability (const Probability& x,
                 ::xml_schema::Flags f = 0,
                 ::xml_schema::Container* c = 0);

    virtual Probability*
    _clone (::xml_schema::Flags f = 0,
            ::xml_schema::Container* c = 0) const;

    virtual 
    ~Probability ();
  };

  class CrispProbability: public ::commonTypes::Probability
  {
    public:
    // val
    //
    typedef ::xml_schema::Double ValType;
    typedef ::xsd::cxx::tree::traits< ValType, char, ::xsd::cxx::tree::schema_type::double_ > ValTraits;

    const ValType&
    val () const;

    ValType&
    val ();

    void
    val (const ValType& x);

    // Constructors.
    //
    CrispProbability (const ValType&);

    CrispProbability (const ::xercesc::DOMElement& e,
                      ::xml_schema::Flags f = 0,
                      ::xml_schema::Container* c = 0);

    CrispProbability (const CrispProbability& x,
                      ::xml_schema::Flags f = 0,
                      ::xml_schema::Container* c = 0);

    virtual CrispProbability*
    _clone (::xml_schema::Flags f = 0,
            ::xml_schema::Container* c = 0) const;

    CrispProbability&
    operator= (const CrispProbability& x);

    virtual 
    ~CrispProbability ();

    // Implementation.
    //
    protected:
    void
    parse (::xsd::cxx::xml::dom::parser< char >&,
           ::xml_schema::Flags);

    protected:
    ::xsd::cxx::tree::one< ValType > val_;
  };

  class DecomposedFuzzyProbability: public ::commonTypes::Probability
  {
    public:
    // alphaCuts
    //
    typedef ::commonTypes::DoubleToIntervalMap AlphaCutsType;
    typedef ::xsd::cxx::tree::sequence< AlphaCutsType > AlphaCutsSequence;
    typedef AlphaCutsSequence::iterator AlphaCutsIterator;
    typedef AlphaCutsSequence::const_iterator AlphaCutsConstIterator;
    typedef ::xsd::cxx::tree::traits< AlphaCutsType, char > AlphaCutsTraits;

    const AlphaCutsSequence&
    alphaCuts () const;

    AlphaCutsSequence&
    alphaCuts ();

    void
    alphaCuts (const AlphaCutsSequence& s);

    // Constructors.
    //
    DecomposedFuzzyProbability ();

    DecomposedFuzzyProbability (const ::xercesc::DOMElement& e,
                                ::xml_schema::Flags f = 0,
                                ::xml_schema::Container* c = 0);

    DecomposedFuzzyProbability (const DecomposedFuzzyProbability& x,
                                ::xml_schema::Flags f = 0,
                                ::xml_schema::Container* c = 0);

    virtual DecomposedFuzzyProbability*
    _clone (::xml_schema::Flags f = 0,
            ::xml_schema::Container* c = 0) const;

    DecomposedFuzzyProbability&
    operator= (const DecomposedFuzzyProbability& x);

    virtual 
    ~DecomposedFuzzyProbability ();

    // Implementation.
    //
    protected:
    void
    parse (::xsd::cxx::xml::dom::parser< char >&,
           ::xml_schema::Flags);

    protected:
    AlphaCutsSequence alphaCuts_;
  };
}

#include <iosfwd>

#include <xercesc/sax/InputSource.hpp>
#include <xercesc/dom/DOMDocument.hpp>
#include <xercesc/dom/DOMErrorHandler.hpp>

namespace commonTypes
{
}

#include <iosfwd>

#include <xercesc/dom/DOMDocument.hpp>
#include <xercesc/dom/DOMErrorHandler.hpp>
#include <xercesc/framework/XMLFormatter.hpp>

#include <xsd/cxx/xml/dom/auto-ptr.hxx>

namespace commonTypes
{
  void
  operator<< (::xercesc::DOMElement&, const Model&);

  void
  operator<< (::xercesc::DOMElement&, const GraphNode&);

  void
  operator<< (::xercesc::DOMElement&, const IdList&);

  void
  operator<< (::xercesc::DOMAttr&, const IdList&);

  void
  operator<< (::xml_schema::ListStream&,
              const IdList&);

  void
  operator<< (::xercesc::DOMElement&, const DoubleToIntervalMap&);

  void
  operator<< (::xercesc::DOMElement&, const Interval&);

  void
  operator<< (::xercesc::DOMElement&, const Issue&);

  void
  operator<< (::xercesc::DOMElement&, const Probability&);

  void
  operator<< (::xercesc::DOMAttr&, const Probability&);

  void
  operator<< (::xml_schema::ListStream&,
              const Probability&);

  void
  operator<< (::xercesc::DOMElement&, const CrispProbability&);

  void
  operator<< (::xercesc::DOMElement&, const DecomposedFuzzyProbability&);
}

#include <xsd/cxx/post.hxx>

// Begin epilogue.
//
//
// End epilogue.

#endif // CXX_ORE_BACK____FRONT_FUZZ_ED_STATIC_XSD_COMMON_H